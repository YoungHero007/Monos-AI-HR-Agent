function downloadSalaryCertificate(){
  const { jsPDF }=window.jspdf;
  const pdf=new jsPDF({format:'a4',unit:'mm'});
  const today=new Date().toISOString().slice(0,10).replaceAll('-','.');
  pdf.setFont('helvetica','bold');
  pdf.setFontSize(18);
  pdf.text('MONOS GROUP',105,28,{align:'center'});
  pdf.setFontSize(14);
  pdf.text('ЦАЛИНГИЙН ТОДОРХОЙЛОЛТ',105,42,{align:'center'});
  pdf.setFont('helvetica','normal');
  pdf.setFontSize(11);
  pdf.text(`Огноо: ${today}`,150,56);
  const rows=[
    ['Ажилтны нэр',employee.fullName],
    ['Ажилтны дугаар',employee.id],
    ['Албан тушаал',employee.position],
    ['Хэлтэс',employee.department],
    ['Ажлын байр',employee.branch],
    ['Сарын үндсэн цалин',employee.salary],
  ];
  let y=76;
  rows.forEach(([label,value])=>{pdf.setFont('helvetica','bold');pdf.text(`${label}:`,30,y);pdf.setFont('helvetica','normal');pdf.text(value,85,y);y+=13;});
  pdf.text('Энэхүү тодорхойлолтыг ажилтны хүсэлтийн дагуу олгов.',30,y+18);
  pdf.text('Хүний нөөцийн алба',30,y+48);
  pdf.save(`tsalingiin-todorhoilolt-${employee.id}.pdf`);
}

document.addEventListener('click',event=>{
  const link=event.target.closest('a[href]');
  if(link&&link.closest('#pageContent')&&link.textContent.includes('Template')){
    event.preventDefault();
    if(window.jspdf)downloadSalaryCertificate();
  }
});
