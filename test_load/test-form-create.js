import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
    stages: [
    { duration: '30s', target: 50 },  // ไต่ระดับไปที่ 50 คนใน 30 วินาที
    { duration: '1m', target: 100 }, // อัดโหลดไปที่ 100 คนต่อเนื่อง 1 นาที
    { duration: '30s', target: 0 },   // ค่อยๆ ลดโหลดลง
    ],
    // vus: 1,          // เริ่มจาก 1 คนก่อนเพื่อดูว่ารอดไหม
    // duration: '30s', // วนลูปยิงเป็นเวลา 30 วินาที
};

export default function () {
    const url = 'https://form.librairy.work/api/create-book-request';
  // สร้าง Payload ตามที่คุณส่งมาในรูปภาพ
    const payload = JSON.stringify({
    firstName: "NATCHANON",
    lastName: "PHATTAMANURUK",
    studentId: "65070501018",
    academicYear: "1",
    author: "ฟลินน์, แคทลีน",
    branch: "mai",
    department: "1",
    email: "natchanon.phat@kmutt.ac.th",
    faculty: "1",
    isbn: "9789740214656",
    publishYear: "",
    publisher: "",
    reason: "Personal interest",
    reasonDescription: "อยากลองเรียนในเรื่องอื่นๆนอกจากวิชาการ",
    remark: "",
    title: "ครัวสุดเก๋ากับศิษย์เก่าเลอ กอร์ดง เบลอ = The kitchen counter cooking school / แค"
    });

    const params = {
    headers: {
        'Content-Type': 'application/json',
      // ถ้าหน้าฟอร์มมีระบบกันบอทหรือต้องการ Session อย่าลืมใส่ Cookie เพิ่มตรงนี้
      // 'Cookie': 'auth_session=...', 
        'User-Agent': 'k6-load-test-agent',
    },
    };

    const res = http.post(url, payload, params);

  // ตรวจสอบความถูกต้องของผลลัพธ์
    check(res, {
    'Status is 200 (Success)': (r) => r.status === 200,
    'Response time < 500ms': (r) => r.timings.duration < 500,
    });

  // จำลองเวลาที่คนใช้กรอกฟอร์มหรือช่วงพักการส่ง (1-2 วินาที)
    sleep(1);
}   