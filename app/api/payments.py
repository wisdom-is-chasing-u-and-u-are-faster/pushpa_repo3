from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/payments", tags=["Payments"])


@router.post("/create-checkout-session")
def create_checkout_session(payload: dict):
    return {
        "session_id": "cs_test_mock_stripe_session_123",
        "checkout_url": "https://checkout.stripe.com/pay/cs_test_mock_stripe_session_123",
        "status": "created"
    }
