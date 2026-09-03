const SALARY_REQUEST_COUNTER='monos_hr_salary_request_counter';

function nextCertificateNumber(){
  const current=Number(localStorage.getItem(SALARY_REQUEST_COUNTER)||0)+1;
  localStorage.setItem(SALARY_REQUEST_COUNTER,String(current));
  return `ЦТ-${new Date().getFullYear()}-${String(current).padStart(4,'0')}`;
}

function prepareSalaryCertificate(){
  const input=document.getElementById('certificatePurpose');
  const purpose=input?.value.trim();
  if(!purpose){input?.focus();alert('Тодорхойлолтыг ямар байгууллага, зориулалтаар авч байгаагаа оруулна уу.');return;}
  const number=nextCertificateNumber();
  const date=new Date().toLocaleDateString('mn-MN');
  const {jsPDF}=window.jspdf;
  const pdf=new jsPDF({format:'a4',unit:'mm'});
  pdf.setFont('helvetica','bold');pdf.setFontSize(17);pdf.text('MONOS GROUP',105,25,{align:'center'});
  pdf.setFontSize(13);pdf.text('SALARY CERTIFICATE',105,38,{align:'center'});
  pdf.setFont('helvetica','normal');pdf.setFontSize(10);pdf.text(`Date: ${date}`,150,52);pdf.text(`No: ${number}`,30,52);
  const rows=[['Employee name',employee.fullName],['Employee ID',employee.id],['Position',employee.position],['Department',employee.department],['Branch',employee.branch],['Monthly salary',employee.salary],['Purpose',purpose]];
  let y=72;rows.forEach(([label,value])=>{pdf.setFont('helvetica','bold');pdf.text(`${label}:`,30,y);pdf.setFont('helvetica','normal');pdf.text(String(value||'-'),78,y);y+=12;});
  pdf.setFontSize(10);pdf.text('This certificate is issued at the employee request.',30,y+12);pdf.text('Executive Director eSign DEMO',30,y+38);pdf.text('Digitally signed for demo purposes',30,y+45);pdf.setDrawColor(33,135,101);pdf.line(30,y+48,92,y+48);
  pdf.save(`salary-certificate-${employee.id}-${number.replaceAll('-','_')}.pdf`);
  if(typeof savePortalSubmission==='function')savePortalSubmission('Цалингийн тодорхойлолт',{purpose,certificateNumber:number,certificateDate:date});
}

function enhanceSalaryPage(){
  const crumb=document.getElementById('pageCrumb');
  const content=document.getElementById('pageContent');
  if(!crumb||!content||crumb.textContent!=='Цалин'||content.querySelector('#certificatePurpose'))return;
  const card=content.querySelector('.module-card');
  if(!card)return;
  const actions=card.querySelector('.form-actions');
  if(!actions)return;
  const field=document.createElement('div');field.className='field full';field.style.marginTop='20px';
  field.innerHTML='<label for="certificatePurpose">Тодорхойлолт авах зориулалт</label><input id="certificatePurpose" type="text" required placeholder="Жишээ: Банкны зээлд материал бүрдүүлэх" />';
  actions.parentElement.insertBefore(field,actions);
  const link=actions.querySelector('a');
  if(link){link.textContent='PDF тодорхойлолт татах';link.removeAttribute('href');link.removeAttribute('download');link.href='#';link.onclick=event=>{event.preventDefault();prepareSalaryCertificate();};}
}

document.addEventListener('DOMContentLoaded',enhanceSalaryPage);
new MutationObserver(enhanceSalaryPage).observe(document.body,{childList:true,subtree:true});
