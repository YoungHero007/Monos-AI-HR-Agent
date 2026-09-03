function applyEmployeeRecord(record){
  const salary=record['Үндсэн цалин']||'0';
  const leaveTotal=Number(record['Жилийн амралтын хоног'])||0;
  const leaveRemaining=Number(record['Үлдсэн амралтын хоног'])||0;
  Object.assign(employee,{name:record['Нэр']||employee.name,fullName:`${record['Овог']||''} ${record['Нэр']||''}`.trim(),id:record.employee_id,position:record['Албан тушаал']||'',department:record['Хэлтэс']||'',branch:record['Салбар']||'',salary:salary.includes('₮')?salary:`${salary} ₮`,leaveTotal,leaveUsed:Math.max(0,leaveTotal-leaveRemaining),leaveRemaining,email:record['Имэйл']||'',phone:record['Утас']||''});
  document.querySelectorAll('.top-user strong,.user-mini strong').forEach(element=>element.textContent=employee.fullName);
  document.querySelectorAll('.top-user small,.user-mini small').forEach(element=>element.textContent=employee.id);
  document.querySelectorAll('.top-user .avatar,.user-mini .avatar').forEach(element=>element.textContent=employee.name.charAt(0));
  const greeting=document.querySelector('#chatMessages .message.bot span');
  if(greeting)greeting.textContent=`Сайн байна уу, ${employee.name}. Танд юугаар туслах вэ?`;
}

document.addEventListener('DOMContentLoaded',()=>{
  const form=document.getElementById('loginForm');
  if(!form||!Array.isArray(window.HR_EMPLOYEES))return;
  form.onsubmit=event=>{
    event.preventDefault();
    const username=document.getElementById('employeeId').value.trim().toUpperCase();
    const password=document.getElementById('password').value;
    const record=window.HR_EMPLOYEES.find(item=>String(item.employee_id).toUpperCase()===username);
    if(!record||password!==String(record.employee_id)){
      alert('Employee ID эсвэл нууц үг буруу байна. Demo нууц үг нь Employee ID-тэй адил байна.');
      return;
    }
    applyEmployeeRecord(record);
    document.getElementById('loginView').classList.add('hidden');
    document.getElementById('appView').classList.remove('hidden');
    render();
  };
});
