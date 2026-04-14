import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 1,          // เริ่มจาก 1 คนก่อนเพื่อดูว่ารอดไหม
  duration: '30s', // วนลูปยิงเป็นเวลา 30 วินาที
};

export default function () {
  const url = 'https://n8n.librairy.work/webhook/test-chatbot';
  
  const payload = JSON.stringify({
    "events": [
      {
        "type": "message",
        "message": {
          "type": "text",
          "id": "609558911020433564",
          "text": "ค้นหาหนังสือเกี่ยวกับ ai"
        },
        "webhookEventId": "01KP5K1PNPTR2Q6YRT63HNNJFJ",
        "deliveryContext": {
          "isRedelivery": true
        },
        "timestamp": 1776156727758,
        "source": {
          "type": "user",
          "userId": "Ud3cf60a08dda274ad89a431817ad9e61"
        },
        "replyToken": "8044e7baac494af981002011e9e9c6a2",
        "mode": "active",
        "destination": "U5770b7ac2b46c3e292176ec8e73c4b4a"
      }
    ]
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
    timeout: '60s', // AI 20B อาจจะใช้เวลานาน ต้องเผื่อเวลาไว้
  };

  const res = http.post(url, payload, params);

  check(res, {
    'status is 200': (r) => r.status === 200,
  });

  sleep(5); // พัก 5 วินาทีก่อนยิงรอบถัดไป
}