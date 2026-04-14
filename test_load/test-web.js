import http from 'k6/http';
import { sleep, check } from 'k6';

export const options = {
    stages: [
    { duration: '30s', target: 50 },  // ไต่ไปที่ 50 คนในครึ่งนาที
    { duration: '1m', target: 100 }, // อัดไปที่ 100 คน (จุดชี้ชะตา)
    { duration: '1m', target: 200 }, // ถ้ายังไม่ล่ม ให้ลอง 200 คน (โหมดทำลายล้าง)
    { duration: '30s', target: 0 },
    ],
};

export default function () {
    const url = 'https://librarian-process-web.librairy.work/api/get-book-requests';
    const params = {
    headers: {
        'Cookie': 'auth_session=14; cf_clearance=DBa9y26aEoXSUxbhpTy4Z6e.wODw6LjbtjVMHcBjwOg-1776160650-1.2.1.1-hHQETHmwh6Jno5QQAwtc2u12RMVi2k6H_79GbOUhLva.DVVeaptZCFcdzmsMFbHCqNBCgLuFsP.4MlIo9RIL643URKPImMCVG.F2Y0VDjFegdR3V0Kt79uzVBcPvtcDxN2TozA3bIE_wnWpSLkhfBc1iJ85QASWl8BG_Ieqsibt4chfT9..ssxnV6yQRqPAKLeXbTuYb56U2jpmZwmWy9Jcdszt7ty89UWW0fMRzNsUUKC1sUv.vJczIa7k9Yuf08JYWBjajqOwRGJLAtE3GG06y7RePlDuiX50dB6HHyhd0WJfc8FLDYqHRLVqrzMRuuDuMKvlKW1b6.Iud7.BeyA',
    },
    };

    const res = http.get(url, params);

    check(res, {
    'status is 200': (r) => r.status === 200,
    'latency check (<500ms)': (r) => r.timings.duration < 500,
    });

  // ลด sleep เหลือแค่ 0.5 วินาที เพื่อเพิ่มแรงกระแทก (RPS)
    sleep(0.5);
}