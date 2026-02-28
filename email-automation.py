#!/usr/bin/env python3
"""
ChooseWow Email Automation System
Bypasses Listmonk list-template limitations by using direct transactional API calls
"""

import requests
import base64
import time
import json
from datetime import datetime, timedelta

# Listmonk Configuration
LISTMONK_URL = "http://localhost:9000"
API_USER = "frank-api"
API_PASS = "1JsVqMPEYicb7yKlQH8n3vzDBLA0y3jP"
CHOOSEWOW_LIST_UUID = "8084bc39-7292-4443-ab90-c09cf4bbbb9e"

# Template IDs
TEMPLATES = {
    "optin": 10,      # Double opt-in confirmation  
    "welcome": 11,    # Welcome + PDF guide
    "story": 12,      # The Habit That Survives
    "bridge": 13      # WowDay bridge
}

# Email sequence timing (days)
SEQUENCE_TIMING = {
    "welcome": 0,     # Immediate after opt-in confirm
    "story": 3,       # 3 days later
    "bridge": 7       # 7 days later
}

def send_transactional_email(subscriber_email, subscriber_name, template_id, extra_data=None):
    """Send transactional email via Listmonk API"""
    
    url = f"{LISTMONK_URL}/api/tx"
    auth = base64.b64encode(f"{API_USER}:{API_PASS}".encode()).decode()
    
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/json"
    }
    
    # Base email data
    email_data = {
        "subscriber_email": subscriber_email,
        "subscriber_name": subscriber_name,
        "template_id": template_id,
        "from_email": "janis@choosewow.com",
        "data": extra_data or {}
    }
    
    try:
        response = requests.post(url, headers=headers, json=email_data, timeout=30)
        if response.status_code == 200:
            print(f"✅ Sent template {template_id} to {subscriber_email}")
            return True
        else:
            print(f"❌ Failed to send template {template_id}: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Email sending error: {e}")
        return False

def send_optin_confirmation(subscriber_email, subscriber_name, optin_url):
    """Send double opt-in confirmation email"""
    return send_transactional_email(
        subscriber_email=subscriber_email,
        subscriber_name=subscriber_name, 
        template_id=TEMPLATES["optin"],
        extra_data={"OptinURL": optin_url}
    )

def send_welcome_sequence(subscriber_email, subscriber_name):
    """Send welcome email with PDF guide"""
    return send_transactional_email(
        subscriber_email=subscriber_email,
        subscriber_name=subscriber_name,
        template_id=TEMPLATES["welcome"],
        extra_data={
            "Subscriber": {
                "FirstName": subscriber_name.split()[0] if subscriber_name else "there"
            }
        }
    )

def send_story_email(subscriber_email, subscriber_name):
    """Send 'The Habit That Survives' story email"""
    return send_transactional_email(
        subscriber_email=subscriber_email,
        subscriber_name=subscriber_name,
        template_id=TEMPLATES["story"],
        extra_data={
            "Subscriber": {
                "FirstName": subscriber_name.split()[0] if subscriber_name else "there"
            }
        }
    )

def send_bridge_email(subscriber_email, subscriber_name):
    """Send WowDay bridge email"""
    return send_transactional_email(
        subscriber_email=subscriber_email,
        subscriber_name=subscriber_name,
        template_id=TEMPLATES["bridge"],
        extra_data={
            "Subscriber": {
                "FirstName": subscriber_name.split()[0] if subscriber_name else "there"
            }
        }
    )

def get_confirmed_subscribers():
    """Get list of confirmed ChooseWow subscribers"""
    url = f"{LISTMONK_URL}/api/subscribers"
    auth = base64.b64encode(f"{API_USER}:{API_PASS}".encode()).decode()
    
    headers = {"Authorization": f"Basic {auth}"}
    params = {
        "list_id": 4,  # ChooseWow list ID
        "status": "enabled",
        "per_page": 100
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        if response.status_code == 200:
            return response.json().get("data", {}).get("results", [])
        else:
            print(f"❌ Failed to get subscribers: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Subscriber fetch error: {e}")
        return []

def test_email_system():
    """Test the email system with a real email"""
    print("🧪 Testing ChooseWow email automation system...")
    
    # Test email
    test_email = "frank.principal.office@gmail.com"
    test_name = "Frank Test"
    
    print(f"📧 Testing welcome email to {test_email}")
    
    # Send welcome email
    success = send_welcome_sequence(test_email, test_name)
    
    if success:
        print("✅ Email automation system working!")
        print("\n📋 Next steps:")
        print("1. Integrate with ChooseWow subscription form")
        print("2. Set up automated sequence (3 & 7 day delays)")
        print("3. Monitor deliverability and engagement")
    else:
        print("❌ Email automation system needs debugging")

def schedule_email_sequence(subscriber_email, subscriber_name, confirmed_date):
    """Schedule the complete email sequence for a subscriber"""
    
    # Immediate: Welcome + PDF
    print(f"📧 Sending welcome email to {subscriber_email}")
    send_welcome_sequence(subscriber_email, subscriber_name)
    
    # Calculate future send dates
    story_date = confirmed_date + timedelta(days=SEQUENCE_TIMING["story"])
    bridge_date = confirmed_date + timedelta(days=SEQUENCE_TIMING["bridge"])
    
    print(f"📅 Story email scheduled for: {story_date.strftime('%Y-%m-%d')}")
    print(f"📅 Bridge email scheduled for: {bridge_date.strftime('%Y-%m-%d')}")
    
    # For now, just log the schedule
    # In production, this would integrate with a job scheduler
    sequence_log = {
        "subscriber_email": subscriber_email,
        "subscriber_name": subscriber_name,
        "confirmed_date": confirmed_date.isoformat(),
        "story_scheduled": story_date.isoformat(),
        "bridge_scheduled": bridge_date.isoformat(),
        "status": "scheduled"
    }
    
    # Save to JSON log file for tracking
    log_file = "/Users/frank/.openclaw/workspace/choosewow/email-sequence-log.json"
    
    try:
        with open(log_file, 'r') as f:
            logs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []
    
    logs.append(sequence_log)
    
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2)
    
    print(f"💾 Sequence logged for {subscriber_email}")

if __name__ == "__main__":
    # Test the system
    test_email_system()
    
    print("\n🚀 ChooseWow Email Automation Ready!")
    print("Use this script to bypass Listmonk template limitations")
    print("All template content is ready - just need proper triggering")