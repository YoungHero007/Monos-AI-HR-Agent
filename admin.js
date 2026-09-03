function adminView(){
  const employees=window.HR_EMPLOYEES||[];
  const requests=typeof getPortalSubmissions==='function'?getPortalSubmissions():[];
  const nameById=Object.fromEntries(employees.map(item=>[item.employee_id,`${item['Овог']||''} ${item['Нэр']||''}`.trim()]));
  const grouped=requests.reduce((groups,item)=>{(groups[item.type||'Бусад хүсэлт']??=[]).push(item);return groups;},{});
  const groupedRows=Object.entries(grouped).map(([type,items])=>`<section class="panel"><div class="panel-head"><h2 class="section-title">${type}</h2><span class="status open">${items.length} хүсэлт</span></div>${items.map(item=>`<div class="activity-row"><div class="activity-icon orange">${icon('file-clock')}</div><div class="activity-info"><strong>${item.employee_name||nameById[item.employee_id]||item.employee_id}</strong><span>${item.employee_id} · ${new Date(item.submitted_at).toLocaleString()} · ${item.request_id}</span></div><span class="status pending">Шинэ</span></div>`).join('')}</section>`).join('')||'<div class="panel"><p>Portal-оор ажилтнаас ирүүлсэн хүсэлт одоогоор алга.</p></div>';
  return page('HR Admin dashboard','Ажилтнаас ирүүлсэн хүсэлтүүдийг төрлөөр ангилсан бүртгэл.',`<div class="content-grid admin-requests">${groupedRows}</div>`);
}

const originalModuleView=moduleView;
moduleView=view=>view==='admin'?adminView():originalModuleView(view);
