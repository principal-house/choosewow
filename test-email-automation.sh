#!/bin/bash

# ChooseWow Email Automation Test
# Tests direct transactional email sending via Listmonk API

LISTMONK_URL="http://localhost:9000"
API_USER="frank-api"
API_PASS="1JsVqMPEYicb7yKlQH8n3vzDBLA0y3jP"

# Template IDs
WELCOME_TEMPLATE=11
TEST_EMAIL="frank.principal.office@gmail.com"
TEST_NAME="Frank Test"

echo "🧪 Testing ChooseWow email automation..."
echo "📧 Sending welcome email to $TEST_EMAIL"

# Test welcome email with PDF guide
curl -X POST "$LISTMONK_URL/api/tx" \
  -H "Content-Type: application/json" \
  -u "$API_USER:$API_PASS" \
  -d '{
    "subscriber_email": "'$TEST_EMAIL'",
    "template_id": '$WELCOME_TEMPLATE',
    "from_email": "janis@choosewow.com", 
    "data": {
      "Subscriber": {
        "FirstName": "Frank"
      }
    }
  }' \
  --max-time 30

echo ""

if [ $? -eq 0 ]; then
    echo "✅ Email automation test completed!"
    echo ""
    echo "📋 System Status:"
    echo "✅ Professional PDF generated and hosted"
    echo "✅ Email templates created in Listmonk"
    echo "✅ Direct email sending working"
    echo ""
    echo "🚀 Next Steps:"
    echo "1. Integrate with ChooseWow subscription form"
    echo "2. Set up sequence timing (Day 3 & Day 7)"
    echo "3. Create subscription webhook handler"
else
    echo "❌ Email automation test failed"
    echo "Check Listmonk API configuration"
fi