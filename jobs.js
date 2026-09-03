const JOBS_URL='https://www.zangia.mn/company/monosgroup';

function jobsView(){return page('Нээлттэй ажлын байр','Monos Group-ийн одоогийн нээлттэй ажлын байруудыг Zangia.mn-ээс хараарай.',`<div class="content-grid"><div class="panel module-card"><div class="panel-head"><div><h2>Monos Group-ийн ажлын байр</h2><p>Ажлын байрны дэлгэрэнгүй мэдээлэл, шаардлага болон бүртгүүлэх үйлдэл Zangia.mn дээр байна.</p></div>${icon('briefcase-business')}</div><div class="activity-row"><div class="activity-icon orange">${icon('building-2')}</div><div class="activity-info"><strong>Monos Group</strong><span>Нээлттэй ажлын байрны жагсаалт</span></div><span class="status open">Zangia.mn</span></div><div class="form-actions"><a class="primary" href="${JOBS_URL}" target="_blank" rel="noopener noreferrer" style="display:inline-flex;align-items:center;justify-content:center;text-decoration:none;">${icon('external-link')} Ажлын байр харах</a></div></div><div class="panel leave-panel"><h2 class="section-title">Анхаарах зүйл</h2><p>Зар бүрийн шаардлага, ажлын байршил, хугацаа болон материалаа Zangia.mn дээрээс шалгана уу.</p></div></div>`);}

const existingModuleView=moduleView;
moduleView=view=>view==='jobs'?jobsView():existingModuleView(view);

document.addEventListener('DOMContentLoaded',()=>{
  document.getElementById('mainNav').insertAdjacentHTML('beforeend',`<button class="nav-item" data-view="jobs"><i data-lucide="briefcase-business"></i><span>Нээлттэй ажлын байр</span></button>`);
  lucide.createIcons();
});
