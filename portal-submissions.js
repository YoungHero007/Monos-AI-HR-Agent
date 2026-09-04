const PORTAL_SUBMISSIONS_KEY='monos_hr_portal_submissions';

function getPortalSubmissions(){
  try{return JSON.parse(localStorage.getItem(PORTAL_SUBMISSIONS_KEY)||'[]');}catch{return[];}
}

function savePortalSubmission(type,fields){
  const submissions=getPortalSubmissions();
  submissions.unshift({request_id:`PORTAL-${Date.now()}`,employee_id:employee.id,employee_name:employee.fullName,type,submitted_at:new Date().toISOString(),fields});
  localStorage.setItem(PORTAL_SUBMISSIONS_KEY,JSON.stringify(submissions));
}

document.addEventListener('submit',event=>{
  const form=event.target;
  if(form.id==='leaveForm'){
    const values=[...form.querySelectorAll('input,select,textarea')].map(field=>field.value);
    savePortalSubmission(values[0]||'Чөлөөний хүсэлт',{leaveType:values[0],totalDays:values[1],startDate:values[2],endDate:values[3],reason:values[4]});
  }
  if(form.id==='hrForm'){
    savePortalSubmission('HR асуулт',{category:form.querySelector('select')?.value,question:form.querySelector('textarea')?.value});
  }
},true);
