const originalOpenMailTo=window.openMailTo;
window.openMailTo=(recipient,subject,body)=>originalOpenMailTo(recipient,subject,`Илгээгчийн имэйл: ${employee.email}\n\n${body}`);
