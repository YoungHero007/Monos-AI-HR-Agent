# Monos HR Employee Portal

Browser-оор шууд нээгддэг demo хувилбар. Одоогийн орчинд Node.js/npm PATH-д байхгүй тул энэ хувилбар нь dependency-free HTML/CSS/JavaScript хэлбэрээр бэлтгэгдсэн.

## Ажиллуулах

`index.html` файлыг browser-оор нээнэ.

Demo login:

- Employee: `EMP001` / `demo123`
- Admin: `admin` / `admin123`

## Одоогийн demo боломжууд

- Employee login screen
- Responsive Monos HR dashboard
- Salary болон certificate flow
- Leave balance болон leave request form
- Schedule
- Orders
- Social insurance
- Personal information update form
- HR question form
- Leave болон HR хүсэлтийг `monosubmonos@gmail.com` руу recipient, subject, body нь бөглөгдсөн email draft болгон нээх
- Admin overview
- Excel import entry point
- Mongolian Monos HR AI chatbot demo
- Suggested questions болон action navigation
- Mobile sidebar болон responsive chat panel

## Файлууд

- `index.html` - application shell
- `styles.css` - responsive UI, brand styling
- `app.js` - demo state, navigation, forms, chatbot logic
- `Monos_HR_Web_Test_Data_100_Employees.xlsx` - supplied test data

## Дараагийн production implementation

Node.js суулгасны дараа Next.js, Prisma, SQLite/PostgreSQL, server-side
session authentication, Zod validation, PDF generation, Excel importer,
HRKnowledge importer болон Gemini/OpenAI provider abstraction-ийг backend
холболттойгоор нэмнэ. Одоогийн хүсэлт илгээх ажиллагаа нь хэрэглэгчийн
default mail application-ийг `mailto:` холбоосоор нээдэг; production-д SMTP
эсвэл transactional email service ашиглан автоматаар илгээх шаардлагатай.
Chatbot нь UI/demo logic бөгөөд production AI API эсвэл database рүү холбогдоогүй.
