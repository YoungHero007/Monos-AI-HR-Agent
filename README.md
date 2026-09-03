# Monos HR Employee Portal

Streamlit дээр ажиллах demo хувилбар. `app.py` нь одоо байгаа HTML/CSS/JavaScript порталыг Streamlit component дотор харуулна.

## Ажиллуулах

```bash
pip install -r requirements.txt
streamlit run app.py
```

Хэрэв dependency суулгахгүйгээр шалгах бол `index.html` файлыг browser-оор шууд нээж болно.

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
- Ажилтны илгээгчийн мэдээлэл: `ulziiuuree22@gmail.com`
- Хүсэлт хүлээн авах HR хаяг: `monosubmonos@gmail.com`
- HR хүсэлт илгээхэд default mail application нээгдэж, илгээгчийн хаяг хүсэлтийн draft-д орно. Бодит `From` account-ийг тухайн mail application-д `ulziiuuree22@gmail.com` болгон тохируулна.
- `Тодорхойлолт загвар.pdf` файлыг salary хэсгийн template татах үйлдэлд холбосон
- `тодорхойлолт.docx` загварт тулгуурлан ажилтны мэдээллээр цалингийн тодорхойлолт PDF үүсгэж татна
- Admin overview
- Excel import entry point
- Mongolian Monos HR AI chatbot demo
- Suggested questions болон action navigation
- Mobile sidebar болон responsive chat panel

## Файлууд

- `app.py` - Streamlit entrypoint
- `requirements.txt` - Streamlit dependency
- `Procfile` - deployment command
- `index.html` - application shell
- `styles.css` - responsive UI, brand styling
- `app.js` - demo state, navigation, forms, chatbot logic
- `jobs.js` - Zangia Monos Group open positions view
- `salary-pdf.js` - employee data-filled salary certificate PDF generator
- `portal-links.js` - Legalinfo chatbot link and E-Mongolia social insurance action
- `pharmacy-logo.css` - Монос Эмийн сан brand styling
- `auth.js` - Excel employee-based login and profile mapping
- `Monos_HR_Web_Test_Data_100_Employees.xlsx` - supplied test data

## Дараагийн production implementation

Node.js суулгасны дараа Next.js, Prisma, SQLite/PostgreSQL, server-side
session authentication, Zod validation, PDF generation, Excel importer,
HRKnowledge importer болон Gemini/OpenAI provider abstraction-ийг backend
холболттойгоор нэмнэ. Одоогийн хүсэлт илгээх ажиллагаа нь хэрэглэгчийн
default mail application-ийг `mailto:` холбоосоор нээдэг; production-д SMTP
эсвэл transactional email service ашиглан автоматаар илгээх шаардлагатай.
Chatbot нь UI/demo logic бөгөөд production AI API эсвэл database рүү холбогдоогүй.
