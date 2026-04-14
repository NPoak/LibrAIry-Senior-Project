import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
    stages: [
    { duration: '30s', target: 50 },  // ไต่ไปที่ 50 คนในครึ่งนาที
    { duration: '1m', target: 100 }, // อัดไปที่ 100 คน (จุดชี้ชะตา)
    { duration: '1m', target: 200 }, // ถ้ายังไม่ล่ม ให้ลอง 200 คน (โหมดทำลายล้าง)
    { duration: '30s', target: 0 },
    ],
};

export default function () {
    const url = 'https://librarian-process-web.librairy.work/api/edit-status-book-requests';
  // สร้าง Array ของสถานะที่เป็นไปได้
    const statuses = ["PENDING_REVIEW", "APPROVE_REVIEW","REJECT_REVIEW"];
  // สุ่มเลือกมา 1 สถานะในทุกครั้งที่ยิง
  const randomStatus = statuses[Math.floor(Math.random() * statuses.length)];

    const payload = JSON.stringify({
    requestId: 134, 
    reviewStatus: randomStatus
    });

    const params = {
    headers: {
            'Content-Type': 'application/json',
        'Cookie': 'auth_session=14; cf_clearance=...', 
    },
    };

    const res = http.post(url, payload, params);

    check(res, {
    'Update สำเร็จ (200)': (r) => r.status === 200,
    });

    sleep(1);
}   