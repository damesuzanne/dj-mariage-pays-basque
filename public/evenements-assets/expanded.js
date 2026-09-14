
document.querySelectorAll('[data-dialog]').forEach(button=>{button.addEventListener('click',()=>document.getElementById(button.dataset.dialog).showModal());});
document.querySelectorAll('dialog').forEach(dialog=>{dialog.querySelectorAll('[data-close]').forEach(button=>button.addEventListener('click',()=>{if(button.dataset.option){const input=document.querySelector('textarea[name="message"]');input.value+=(input.value?'\n':'')+'Prestation souhaitée : '+button.dataset.option;}dialog.close();}));dialog.addEventListener('click',event=>{if(event.target===dialog){const r=dialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)dialog.close();}});});
const form=document.getElementById('quote-form');const status=document.getElementById('form-status');
form.addEventListener('submit',async event=>{
 event.preventDefault();if(!form.reportValidity())return;
 const button=form.querySelector('[type="submit"]');if(button.disabled)return;
 const data=new FormData(form);if(data.get('botcheck'))return;
 button.disabled=true;status.hidden=false;status.textContent='Envoi en cours…';
 try{
  const verification=await fetch('/api/contact/verify',{method:'POST',body:data});
  const verified=await verification.json();
  if(!verification.ok||!verified.success)throw new Error(verified.message||'Veuillez vérifier la protection antispam.');
  data.delete('cf-turnstile-response');data.delete('botcheck');
  data.set('access_key','3f6d1840-64d1-4521-bb72-95d8b95071e5');
  data.set('subject','Demande de devis : '+eventCategory);
  data.set('from_name','Richard DJ Event');data.set('name',data.get('prenom')+' '+data.get('nom'));
  const response=await fetch('https://api.web3forms.com/submit',{method:'POST',body:data});
  const result=await response.json();if(!response.ok||!result.success)throw new Error('Votre demande n’a pas pu être envoyée. Réessayez ou contactez Richard par WhatsApp.');
  status.textContent='Votre demande a bien été envoyée à Richard. Merci !';form.reset();
 }catch(error){status.textContent=error.message||'Envoi impossible. Vous pouvez contacter Richard par WhatsApp ou au 06 84 33 18 24.';}
 finally{button.disabled=false;if(window.turnstile)window.turnstile.reset();}
});
document.getElementById('whatsapp-send').addEventListener('click',()=>{if(!form.reportValidity())return;const data=Object.fromEntries(new FormData(form));const labels={organisation:'Organisation',date:'Date envisagée',lieu:'Lieu',participants:'Participants',horaires:'Horaires',telephone:'Téléphone',email:'Email',message:'Projet'};const lines=['Bonjour Richard,','Je souhaite une proposition pour '+eventCategory+'.','Nom : '+data.prenom+' '+data.nom];Object.entries(labels).forEach(([key,label])=>{if(data[key])lines.push(label+' : '+data[key]);});window.open('https://wa.me/33684331824?text='+encodeURIComponent(lines.join('\n')),'_blank','noopener');status.hidden=false;status.textContent='Votre message est prêt à être vérifié et envoyé dans WhatsApp.';});
