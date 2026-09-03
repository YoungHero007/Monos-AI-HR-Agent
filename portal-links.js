const LEGALINFO_LINK='https://legalinfo.mn/mn';
const EMONGOLIA_LINK='https://e-mongolia.mn/';

function addPortalLinks(){
  const chatMessages=document.getElementById('chatMessages');
  if(chatMessages&&!chatMessages.querySelector('.portal-link-suggestion')){
    const link=document.createElement('a');
    link.className='suggestions portal-link-suggestion';
    link.href=LEGALINFO_LINK;
    link.target='_blank';
    link.rel='noopener noreferrer';
    link.textContent='Эрх зүйн мэдээлэл авах';
    chatMessages.appendChild(link);
  }

  const pageContent=document.getElementById('pageContent');
  const crumb=document.getElementById('pageCrumb');
  if(pageContent&&crumb&&crumb.textContent==='Нийгмийн даатгал'&&!pageContent.querySelector('.emongolia-link')){
    const panel=document.createElement('div');
    panel.className='panel emongolia-link';
    panel.innerHTML=`<div class="panel-head"><h2 class="section-title">Нийгмийн даатгалын шимтгэл төлөлт</h2>${icon('external-link')}</div><p>Өөрийн шимтгэл төлөлтийн дэлгэрэнгүй мэдээллийг Цахим үйлчилгээний нэгдсэн порталаас авна уу.</p><div class="form-actions"><a class="primary" href="${EMONGOLIA_LINK}" target="_blank" rel="noopener noreferrer" style="display:inline-flex;align-items:center;justify-content:center;text-decoration:none;">${icon('external-link')} Шимтгэл төлөлт авах</a></div>`;
    pageContent.appendChild(panel);
    lucide.createIcons();
  }
}

document.addEventListener('DOMContentLoaded',()=>{
  addPortalLinks();
  new MutationObserver(addPortalLinks).observe(document.getElementById('pageContent'),{childList:true,subtree:true});
});
