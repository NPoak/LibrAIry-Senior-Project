import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
stages: [
    { duration: '30s', target: 50 },  // ไต่ระดับไปที่ 50 คนพร้อมกัน
    { duration: '1m', target: 100 }, // รันค้างไว้ที่ 100 คนเพื่อดูความนิ่ง
    { duration: '30s', target: 0 },   // ค่อยๆ ลดโหลดลง
],
};

export default function () {
const url = 'https://form.librairy.work/api/get-my-request';
  // Payload ที่ส่ง requesterID ตามรูปภาพที่คุณแคปมา
const payload = JSON.stringify({
    requesterID: "65070501018"
});

const params = {
    headers: {
    'Content-Type': 'application/json',
    'User-Agent': 'k6-load-test-agent',
      // หาก API นี้มีการเช็ค Authorization อย่าลืมใส่เพิ่มครับ
      // 'Authorization': 'Bearer <TOKEN>',
    },
};

const res = http.post(url, payload, params);

  // ตรวจสอบความถูกต้อง
check(res, {
    'Status is 200 (OK)': (r) => r.status === 200,
    'Response is JSON': (r) => r.headers['Content-Type'].includes('application/json'),
    'Has requestInfo': (r) => {
    const body = JSON.parse(r.body);
    return body.status === 'success' && Array.isArray(body.requestInfo);
    },
    'Response time < 300ms': (r) => r.timings.duration < 300,
});

  // จำลองพฤติกรรมผู้ใช้ (ดูรายการคำขอครู่หนึ่งก่อน Refresh)
sleep(1.5);
}

