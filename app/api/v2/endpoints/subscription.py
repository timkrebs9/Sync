from fastapi import APIRouter, Depends, Header, Request, HTTPException, Response
from fastapi.responses import RedirectResponse
from app.services.stripe_service import stripe_service
from app.core.security import get_current_user
from app.crud import user_crud
from app.models.user_model import User, SubscriptionTier
from datetime import datetime
from sqlalchemy.orm import Session
from app.core.database import get_db
import stripe

router = APIRouter()

@router.post("/create-checkout-session")
async def create_checkout_session(
    current_user: User = Depends(get_current_user)
):
    try:
        session_id = await stripe_service.create_checkout_session(current_user.id)
        return {"session_id": session_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/cancel")
async def cancel_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.stripe_subscription_id:
        raise HTTPException(status_code=400, detail="No active subscription found")
    
    try:
        await stripe_service.cancel_subscription(current_user.stripe_subscription_id)
        await user_crud.update_subscription_status(
            db,
            user_id=current_user.id,
            subscription_tier=SubscriptionTier.FREE,
            subscription_end_date=datetime.now()
        )
        return {"message": "Subscription cancelled successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/success")
async def subscription_success(
    session_id: str,
    db: Session = Depends(get_db)
):
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        # Update user subscription details
        await user_crud.update_subscription_status(
            db,
            user_id=int(session.client_reference_id),
            subscription_tier=SubscriptionTier.PREMIUM,
            stripe_subscription_id=session.subscription
        )
        return RedirectResponse(url="/")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/webhook")
async def webhook_received(
    request: Request,
    stripe_signature: str = Header(None),
    db: Session = Depends(get_db)
):
    try:
        payload = await request.body()
        event = await stripe_service.handle_webhook(payload, stripe_signature)
        
        # Handle different types of webhook events
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            # Update user subscription status to premium
            await user_crud.update_subscription_status(
                db,
                user_id=int(session.client_reference_id),
                subscription_tier=SubscriptionTier.PREMIUM,
                stripe_subscription_id=session.subscription
            )
            
        elif event['type'] == 'customer.subscription.deleted':
            subscription = event['data']['object']
            # Update user subscription status to free
            await user_crud.update_subscription_status(
                db,
                user_id=int(subscription.metadata.user_id),
                subscription_tier=SubscriptionTier.FREE,
                subscription_end_date=datetime.now()
            )
            
        elif event['type'] == 'invoice.payment_failed':
            # Handle failed payments
            subscription = event['data']['object']
            await user_crud.update_subscription_status(
                db,
                user_id=int(subscription.metadata.user_id),
                subscription_tier=SubscriptionTier.FREE
            )
            
        return {"status": "success"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) 