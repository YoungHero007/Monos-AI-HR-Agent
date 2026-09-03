const SENDER_EMAIL='ulziiuuree22@gmail.com';
const HR_RECIPIENT='monosubmonos@gmail.com';
window.openMailTo=(recipient,subject,body)=>{
	const params=new URLSearchParams({view:'cm',fs:'1',to:recipient||HR_RECIPIENT,su:subject,body:`Илгээгчийн имэйл: ${employee.email||SENDER_EMAIL}\n\n${body}`});
	window.open(`https://mail.google.com/mail/?authuser=${encodeURIComponent(SENDER_EMAIL)}&${params.toString()}`,'_blank','noopener,noreferrer');
};
