function adminView(){
  const employees=window.HR_EMPLOYEES||[];
  const requests=window.HR_REQUESTS||[];
  const certificates=window.HR_CERTIFICATES||[];
  const nameById=Object.fromEntries(employees.map(item=>[item.employee_id,`${item['Овог']||''} ${item['Нэр']||''}`.trim()]));
  const requestRows=requests.map(item=>`<div class="activity-row"><div class="activity-icon orange">${icon('file-clock')}</div><div class="activity-info"><strong>${nameById[item.employee_id]||item.employee_id}</strong><span>${item['Чөлөөний төрөл']||'Хүсэлт'} · ${item['Эхлэх огноо']||''} · ${item.request_id}</span></div><span class="status ${item['Төлөв']==='Хүлээгдэж буй'?'pending':'approved'}">${item['Төлөв']||'Бүртгэлтэй'}</span></div>`).join('')||'<p>Хүсэлтийн бүртгэл одоогоор алга.</p>';
  const certificateRows=certificates.map(item=>`<div class="activity-row"><div class="activity-icon blue">${icon('file-check-2')}</div><div class="activity-info"><strong>${nameById[item.employee_id]||item.employee_id}</strong><span>Цалингийн тодорхойлолт · ${item['Он сар']||''} · ${item.salary_id}</span></div><strong>${item['Үндсэн цалин']?Number(item['Үндсэн цалин']).toLocaleString()+' ₮':'-'}</strong></div>`).join('')||'<p>Тодорхойлолтын бүртгэл одоогоор алга.</p>';
  return page('HR Admin dashboard','Ажилтнаас ирүүлсэн хүсэлт болон тодорхойлолтын бүртгэл.',`<div class="admin-kpis"><article class="admin-kpi"><span>Нийт ажилтан</span><strong>${employees.length}</strong></article><article class="admin-kpi"><span>Нийт хүсэлт</span><strong>${requests.length}</strong></article><article class="admin-kpi"><span>Тодорхойлолт</span><strong>${certificates.length}</strong></article></div><div class="content-grid"><div class="panel"><div class="panel-head"><h2 class="section-title">Ажилтны хүсэлтүүд</h2><span class="status open">request_id</span></div>${requestRows}</div><div class="panel"><div class="panel-head"><h2 class="section-title">Тодорхойлолтын бүртгэл</h2><span class="status open">salary_id</span></div>${certificateRows}</div></div>`);
}

const originalModuleView=moduleView;
moduleView=view=>view==='admin'?adminView():originalModuleView(view);
