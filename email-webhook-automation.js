// ChooseWow Email Automation Webhook
// Triggers email sequence when someone subscribes via choosewow.com form

const LISTMONK_URL = "https://mail.principal.house";
const CHOOSEWOW_LIST_UUID = "8084bc39-7292-4443-ab90-c09cf4bbbb9e";

// Email sequence templates
const EMAIL_TEMPLATES = {
  welcome: 11,    // Welcome + PDF guide (immediate)
  story: 12,      // The Habit That Survives (Day 3)  
  bridge: 13      // WowDay Bridge (Day 7)
};

async function sendEmailViaListmonk(subscriberEmail, templateId, data = {}) {
  console.log(`📧 Sending template ${templateId} to ${subscriberEmail}`);
  
  // This would use admin credentials or proper SMTP setup
  const response = await fetch(`${LISTMONK_URL}/api/tx`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa('admin:PASSWORD') // Use admin creds
    },
    body: JSON.stringify({
      subscriber_email: subscriberEmail,
      template_id: templateId,
      from_email: 'janis@choosewow.com',
      data: data
    })
  });
  
  return response.ok;
}

export async function handleChooseWowSubscription(email, name) {
  console.log(`🎯 New ChooseWow subscriber: ${email}`);
  
  // Send immediate welcome email with PDF
  await sendEmailViaListmonk(email, EMAIL_TEMPLATES.welcome, {
    Subscriber: { 
      FirstName: name?.split(' ')[0] || 'there' 
    }
  });
  
  // Schedule follow-up emails (would use cron/scheduler in production)
  scheduleEmail(email, name, EMAIL_TEMPLATES.story, 3);   // Day 3
  scheduleEmail(email, name, EMAIL_TEMPLATES.bridge, 7);  // Day 7
  
  console.log(`✅ Email sequence initiated for ${email}`);
}

function scheduleEmail(email, name, templateId, delayDays) {
  // This would integrate with a job scheduler (cron, etc.)
  console.log(`⏰ Scheduled template ${templateId} for ${email} in ${delayDays} days`);
  
  // For now, log to a JSON file for manual processing
  const scheduleLog = {
    email,
    name,
    templateId, 
    sendDate: new Date(Date.now() + delayDays * 24 * 60 * 60 * 1000).toISOString(),
    status: 'scheduled'
  };
  
  // Would save to database/file for processing
  console.log('Schedule entry:', scheduleLog);
}

// Integration with choosewow.com subscription form
// This function would be called when the form is submitted
export function wireToChooseWowForm() {
  console.log(`
🔧 TO WIRE TO CHOOSEWOW.COM FORM:

1. Update choosewow form submit handler to call:
   handleChooseWowSubscription(email, name)

2. Current form location: choosewow.com homepage
   
3. Form already posts to Listmonk, need to add webhook trigger

4. Templates ready: ${Object.values(EMAIL_TEMPLATES).join(', ')}
  `);
}