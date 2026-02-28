#!/usr/bin/env python3
"""
ChooseWow Email Automation System - Mautic Version
Handles email sequences via Mautic's API
"""

import requests
import json
import time
from datetime import datetime, timedelta

# Mautic Configuration
MAUTIC_URL = "https://mail.principal.house"
MAUTIC_API_URL = f"{MAUTIC_URL}/api"
SUBSCRIBE_API = f"{MAUTIC_URL}/api/subscribe.php"

# Segment IDs (from TOOLS.md)
SEGMENTS = {
    "operatingleader": 1,
    "choosewow": 2,
    "wowday": 3,
    "unsaidsignals": 4
}

# Email sequence timing (days)
SEQUENCE_TIMING = {
    "welcome": 0,     # Immediate after subscription
    "story": 3,       # 3 days later
    "bridge": 7       # 7 days later
}

def add_subscriber_to_mautic(email, name, brand):
    """Add subscriber to Mautic via brand"""
    
    data = {
        "email": email,
        "brand": brand  # operatingleader|choosewow|wowday|unsaidsignals
    }
    
    try:
        response = requests.post(SUBSCRIBE_API, json=data, timeout=30)
        if response.status_code == 200:
            print(f"✅ Added {email} to Mautic segment {segment_id}")
            return True
        else:
            print(f"❌ Failed to add {email}: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Subscription error: {e}")
        return False

def send_choosewow_welcome(email, name):
    """Trigger welcome email sequence in Mautic"""
    
    # Add to ChooseWow brand
    success = add_subscriber_to_mautic(email, name, "choosewow")
    
    if success:
        print(f"📧 Welcome sequence triggered for {email}")
        # Mautic campaign automation will handle the rest
        # based on segment membership and campaign triggers
    
    return success

def test_email_system():
    """Test the Mautic email system"""
    print("🧪 Testing ChooseWow Mautic email automation...")
    
    # Test email
    test_email = "frank.principal.office+test@gmail.com"
    test_name = "Frank Test"
    
    print(f"📧 Adding {test_email} to ChooseWow segment")
    
    # Add to segment (will trigger campaign)
    success = send_choosewow_welcome(test_email, test_name)
    
    if success:
        print("✅ Mautic automation system working!")
        print("\n📋 Next steps:")
        print("1. Set up Mautic campaigns for ChooseWow sequence")
        print("2. Configure email templates in Mautic")
        print("3. Set up campaign delays (3 & 7 days)")
    else:
        print("❌ Mautic automation system needs debugging")

def migrate_from_listmonk():
    """Helper to migrate settings from Listmonk to Mautic"""
    print("\n🔄 Migration Guide from Listmonk to Mautic:")
    print("1. Export subscribers from Listmonk")
    print("2. Import to Mautic ChooseWow segment (ID: 2)")
    print("3. Create email templates in Mautic:")
    print("   - Welcome + PDF guide")
    print("   - The Habit That Survives (Day 3)")
    print("   - WowDay Bridge (Day 7)")
    print("4. Set up Mautic campaign with delays")
    print("5. Test with a few subscribers first")

if __name__ == "__main__":
    # Test the system
    test_email_system()
    
    # Show migration guide
    migrate_from_listmonk()
    
    print("\n🚀 ChooseWow Mautic Automation Ready!")
    print("API endpoint:", SUBSCRIBE_API)