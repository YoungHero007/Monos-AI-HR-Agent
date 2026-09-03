function applyEmployeeRecord(record){
  const salary=record['Үндсэн цалин']||'0';
  const leaveTotal=Number(record['Жилийн амралтын хоног'])||0;
  const leaveRemaining=Number(record['Үлдсэн амралтын хоног'])||0;
  const workedYears=Number(record['Ажилласан жил'])||0;
  Object.assign(employee,{name:record['Нэр']||employee.name,fullName:`${record['Овог']||''} ${record['Нэр']||''}`.trim(),id:record.employee_id,position:record['Албан тушаал']||'',department:record['Хэлтэс']||'',branch:record['Салбар']||'',salary:salary.includes('₮')?salary:`${Number(salary).toLocaleString()} ₮`,leaveTotal,leaveUsed:Math.max(0,leaveTotal-leaveRemaining),leaveRemaining,workedYears,email:record['Имэйл']||'',phone:record['Утас']||''});
  document.querySelectorAll('.top-user strong,.user-mini strong').forEach(element=>element.textContent=employee.fullName);
  document.querySelectorAll('.top-user small,.user-mini small').forEach(element=>element.textContent=employee.id);
  document.querySelectorAll('.top-user .avatar,.user-mini .avatar').forEach(element=>element.textContent=employee.name.charAt(0));
  const greeting=document.querySelector('#chatMessages .message.bot span');
  if(greeting)greeting.textContent=`Сайн байна уу, ${employee.name}. Танд юугаар туслах вэ?`;
}

function refreshEmployeeNumbers(){
  const values=document.querySelectorAll('.stat-card .stat-value');
  if(values[0])values[0].textContent=employee.salary;
  if(values[1])values[1].textContent=employee.leaveRemaining;
  if(values[3])values[3].textContent=employee.workedYears;
  const workedLabel=document.querySelectorAll('.stat-card .stat-sub')[3];
  if(workedLabel)workedLabel.textContent='жил ажилласан';
  document.querySelectorAll('.module-card .activity-info strong').forEach(element=>{if(element.textContent==='Үндсэн цалин')element.parentElement.nextElementSibling.textContent=employee.salary;});
}

document.addEventListener('DOMContentLoaded',()=>{
  const form=document.getElementById('loginForm');
  if(!form||!Array.isArray(window.HR_EMPLOYEES))return;
  const demoCredentials=document.querySelector('.demo-note span');
  if(demoCredentials)demoCredentials.textContent='Employee: EMP001 / EMP001 · HR Admin: HR001 / HR001';
  form.onsubmit=event=>{
    event.preventDefault();
    const username=document.getElementById('employeeId').value.trim().toUpperCase();
    const password=document.getElementById('password').value;
    if(username==='HR001'&&password==='HR001'){
      employee.name='HR Admin';
      employee.fullName='Хүний нөөцийн админ';
      employee.id='HR001';
      employee.position='HR Administrator';
      document.getElementById('loginView').classList.add('hidden');
      document.getElementById('appView').classList.remove('hidden');
      render('admin');
      return;
    }
    const record=window.HR_EMPLOYEES.find(item=>String(item.employee_id).toUpperCase()===username);
    if(!record||password!==String(record.employee_id)){
      alert('Employee ID эсвэл нууц үг буруу байна. Demo нууц үг нь Employee ID-тэй адил байна.');
      return;
    }
    applyEmployeeRecord(record);
    document.getElementById('loginView').classList.add('hidden');
    document.getElementById('appView').classList.remove('hidden');
    render();
    refreshEmployeeNumbers();
  };
});
