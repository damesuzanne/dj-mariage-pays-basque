// Version anglaise de expanded.js (pages /en/corporate-events/ et /en/bars-restaurants/), 07/10/26.

document.querySelectorAll('[data-dialog]').forEach(button=>{button.addEventListener('click',()=>document.getElementById(button.dataset.dialog).showModal());});
document.querySelectorAll('dialog').forEach(dialog=>{dialog.querySelectorAll('[data-close]').forEach(button=>button.addEventListener('click',()=>{if(button.dataset.option){const input=document.querySelector('textarea[name="message"]');input.value+=(input.value?'\n':'')+'Service requested: '+button.dataset.option;}dialog.close();}));dialog.addEventListener('click',event=>{if(event.target===dialog){const r=dialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)dialog.close();}});});
const form=document.getElementById('quote-form');const status=document.getElementById('form-status');
form.addEventListener('submit',async event=>{
 event.preventDefault();if(!form.reportValidity())return;
 const button=form.querySelector('[type="submit"]');if(button.disabled)return;
 const data=new FormData(form);if(data.get('botcheck'))return;
 button.disabled=true;status.hidden=false;status.textContent='Sending…';
 try{
  const verification=await fetch('/api/contact/verify',{method:'POST',body:data});
  const verified=await verification.json();
  if(!verification.ok||!verified.success)throw new Error(verified.message||'Please complete the anti-spam check.');
  data.delete('cf-turnstile-response');data.delete('botcheck');
  data.set('access_key','3f6d1840-64d1-4521-bb72-95d8b95071e5');
  data.set('subject', '🚨 ALERTE CONTACT: NOUVEAU MESSAGE SITE !');
  data.set("Site d’origine", "Pays Basque, version anglaise : https://djmariagepaysbasque.fr/en/");data.set('Langue','Anglais (demande envoyée depuis la version anglaise du site)');
  data.set('from_name',"NOUVEAU CONTACT DJ MARIAGE");data.set('name',data.get('prenom')+' '+data.get('nom'));
  const response=await fetch('https://api.web3forms.com/submit',{method:'POST',body:data});
  const result=await response.json();if(!response.ok||!result.success)throw new Error('Your request could not be sent. Please try again or contact Richard on WhatsApp.');
  status.textContent='Thank you, your request has been sent to Richard!';form.reset();
 }catch(error){status.textContent=error.message||'Sending failed. You can reach Richard on WhatsApp or at +33 6 84 33 18 24.';}
 finally{button.disabled=false;if(window.turnstile)window.turnstile.reset();}
});
document.getElementById('whatsapp-send').addEventListener('click',()=>{if(!form.reportValidity())return;const data=Object.fromEntries(new FormData(form));const labels={organisation:'Organisation',date:'Preferred date',lieu:'Venue',participants:'Guests',horaires:'Times',telephone:'Phone',email:'Email',message:'Plans'};const lines=['Hello Richard,','I would like a proposal for '+eventCategory+'.','Name: '+data.prenom+' '+data.nom];Object.entries(labels).forEach(([key,label])=>{if(data[key])lines.push(label+': '+data[key]);});window.open('https://wa.me/33684331824?text='+encodeURIComponent(lines.join('\n')),'_blank','noopener');status.hidden=false;status.textContent='Your message is ready to check and send in WhatsApp.';});
