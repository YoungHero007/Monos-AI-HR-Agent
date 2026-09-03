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

- HR Admin dashboard-оос portal хүсэлтүүдийг Excel файлаар татна
- HR Admin dashboard дээр цалин, амралт/чөлөө, тушаалын огноо болон дугаарын бүртгэл харагдана
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
- `admin.js` - HR001 admin dashboard with request and certificate registers
- `Monos_HR_Web_Test_Data_100_Employees.xlsx` - supplied test data

## Дараагийн production implementation

Node.js суулгасны дараа Next.js, Prisma, SQLite/PostgreSQL, server-side
session authentication, Zod validation, PDF generation, Excel importer,
HRKnowledge importer болон Gemini/OpenAI provider abstraction-ийг backend
холболттойгоор нэмнэ. Одоогийн хүсэлт илгээх ажиллагаа нь хэрэглэгчийн
Gmail compose цонх нээгдэж, `From` account `ulziiuuree22@gmail.com`, `To` account
`monosubmonos@gmail.com` болон хүсэлтийн мэдээлэл автоматаар бөглөгдөнө. Gmail
дээр `Send` дарж илгээнэ; production-д SMTP
эсвэл transactional email service ашиглан автоматаар илгээх шаардлагатай.
Chatbot нь UI/demo logic бөгөөд production AI API эсвэл database рүү холбогдоогүй.
