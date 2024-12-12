import stripe
from app.core.config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeService:
    @staticmethod
    async def create_checkout_session(user_id: int):
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': settings.STRIPE_PRICE_ID,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=f'{settings.FRONTEND_URL}/subscription/success?session_id={{CHECKOUT_SESSION_ID}}',
                cancel_url=f'{settings.FRONTEND_URL}/subscription/cancel',
                client_reference_id=str(user_id),
            )
            return checkout_session
        except stripe.error.StripeError as e:
            raise ValueError(f"Stripe error: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error creating checkout session: {str(e)}")

    @staticmethod
    async def cancel_subscription(subscription_id: str):
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)
            stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=True
            )
            return subscription
        except Exception as e:
            raise ValueError(f"Error canceling subscription: {str(e)}")

    @staticmethod
    async def handle_webhook(payload: bytes, signature: str):
        try:
            event = stripe.Webhook.construct_event(
                payload, signature, settings.STRIPE_WEBHOOK_SECRET
            )
            return event
        except Exception as e:
            raise ValueError(f"Error validating webhook: {str(e)}")

stripe_service = StripeService() 