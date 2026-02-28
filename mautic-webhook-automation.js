// ChooseWow Email Automation Webhook - Mautic Version
// Triggers email sequence when someone subscribes via choosewow.com form

const MAUTIC_URL = "https://mail.principal.house";
const SUBSCRIBE_API = `${MAUTIC_URL}/api/subscribe.php`;
const CHOOSEWOW_SEGMENT_ID = 2;

async function addToMauticBrand(email, brand) {
  console.log(`📧 Adding ${email} to Mautic brand ${brand}`);
  
  const response = await fetch(SUBSCRIBE_API, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      email: email,
      brand: brand
    })
  });
  
  return response.ok;
}

export async function handleChooseWowSubscription(email, name) {
  console.log(`🎯 New ChooseWow subscriber: ${email}`);
  
  // Add to ChooseWow brand in Mautic
  const success = await addToMauticBrand(email, "choosewow");
  
  if (success) {
    console.log(`✅ ${email} added to Mautic - campaign automation will handle the sequence`);
    // Mautic campaigns handle:
    // - Immediate: Welcome email with PDF
    // - Day 3: The Habit That Survives
    // - Day 7: WowDay Bridge
  } else {
    console.error(`❌ Failed to add ${email} to Mautic`);
  }
  
  return success;
}

// Integration with choosewow.com subscription form
export function wireToChooseWowForm() {
  console.log(`
🔧 TO WIRE TO CHOOSEWOW.COM FORM:

1. Update form action to POST to:
   ${SUBSCRIBE_API}
   
2. Form data format:
   {
     "email": "subscriber@email.com",
     "name": "Subscriber Name",
     "segment_id": 2
   }

3. Or call handleChooseWowSubscription() from your form handler

4. Mautic campaign will automatically handle the email sequence
`);
}

// For Cloudflare Workers deployment
export default {
  async fetch(request) {
    if (request.method === 'POST') {
      const data = await request.json();
      const { email, name } = data;
      
      if (email) {
        const success = await handleChooseWowSubscription(email, name || '');
        
        return new Response(JSON.stringify({ success }), {
          headers: { 'Content-Type': 'application/json' }
        });
      }
    }
    
    return new Response('Method not allowed', { status: 405 });
  }
};