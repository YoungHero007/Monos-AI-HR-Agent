function adminView(){
  const employees=window.HR_EMPLOYEES||[];
  const requests=typeof getPortalSubmissions==='function'?getPortalSubmissions():[];
  const nameById=Object.fromEntries(employees.map(item=>[item.employee_id,`${item['Овог']||''} ${item['Нэр']||''}`.trim()]));
  const grouped=requests.reduce((groups,item)=>{(groups[item.type||'Бусад хүсэлт']??=[]).push(item);return groups;},{});
  const groupedRows=Object.entries(grouped).map(([type,items])=>`<section class="panel"><div class="panel-head"><h2 class="section-title">${type}</h2><span class="status open">${items.length} хүсэлт</span></div>${items.map(item=>`<div class="activity-row"><div class="activity-icon orange">${icon('file-clock')}</div><div class="activity-info"><strong>${item.employee_name||nameById[item.employee_id]||item.employee_id}</strong><span>${item.employee_id} · ${new Date(item.submitted_at).toLocaleString()} · ${item.request_id}</span></div><span class="status pending">Шинэ</span></div>`).join('')}</section>`).join('')||'<div class="panel"><p>Portal-оор ажилтнаас ирүүлсэн хүсэлт одоогоор алга.</p></div>';
  return page('HR Admin dashboard','Ажилтнаас ирүүлсэн хүсэлтүүдийг төрлөөр ангилсан бүртгэл.',`<div class="form-actions" style="margin-bottom:20px"><button class="primary" id="exportRequestsButton" type="button">${icon('download')} Excel файлаар татах</button></div><div class="content-grid admin-requests">${groupedRows}</div>`);
}

function exportPortalRequests(){
  const submissions=typeof getPortalSubmissions==='function'?getPortalSubmissions():[];
  if(!submissions.length){alert('Татах portal хүсэлтийн бүртгэл одоогоор алга.');return;}
  if(!window.XLSX){alert('Excel таталтын сан ачаалагдаагүй байна. Дахин оролдоно уу.');return;}
  const rows=submissions.map(item=>({
    'Хүсэлтийн дугаар':item.request_id,
    'Ажилтны нэр':item.employee_name,
    'Ажилтны ID':item.employee_id,
    'Хүсэлтийн төрөл':item.type,
    'Илгээсэн огноо':new Date(item.submitted_at).toLocaleString(),
    'Чөлөөний төрөл':item.fields?.leaveType||'',
    'Нийт хоног':item.fields?.totalDays||'',
    'Эхлэх огноо':item.fields?.startDate||'',
    'Дуусах огноо':item.fields?.endDate||'',
    'Шалтгаан / асуулт':item.fields?.reason||item.fields?.question||'',
    'Ангилал':item.fields?.category||'',
    'Төлөв':'Шинэ'
  }));
  const workbook=XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook,XLSX.utils.json_to_sheet(rows),'Portal хүсэлтүүд');
  XLSX.writeFile(workbook,`monos-hr-portal-requests-${new Date().toISOString().slice(0,10)}.xlsx`);
}

document.addEventListener('click',event=>{if(event.target.closest('#exportRequestsButton'))exportPortalRequests();});

const originalModuleView=moduleView;
moduleView=view=>view==='admin'?adminView():originalModuleView(view);
