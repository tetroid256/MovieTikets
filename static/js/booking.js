/* --- htmlから分割 --- */
// --- データ保持用 ---
let bookingData = {
    date: "",
    time: "",
    seats: [], 
    passengers: [] 
};

// --- カレンダー用状態変数 ---
const realToday = new Date(); 
let displayYear = realToday.getFullYear(); 
let displayMonth = realToday.getMonth();

// --- 初期化 ---
window.onload = function() {
    renderCalendar();
    renderSeats();
    calcEndTimes(); 
};

// --- STEP 1: カレンダー & 時間 ---
function changeMonth(diff) {
    displayMonth += diff;
    if (displayMonth > 11) { displayMonth = 0; displayYear++; } 
    else if (displayMonth < 0) { displayMonth = 11; displayYear--; }
    renderCalendar();
}

function renderCalendar() {
    document.getElementById('calMonth').innerText = `${displayYear}年 ${displayMonth + 1}月`;
    const grid = document.getElementById('calGrid');
    grid.innerHTML = ""; 

    const btnPrev = document.getElementById('btnPrevMonth');
    const isCurrentMonth = (displayYear === realToday.getFullYear() && displayMonth === realToday.getMonth());
    
    if (displayYear < realToday.getFullYear() || (displayYear === realToday.getFullYear() && displayMonth <= realToday.getMonth())) {
            btnPrev.disabled = true;
    } else {
            btnPrev.disabled = false;
    }

    const firstDayObj = new Date(displayYear, displayMonth, 1);
    const startDayOfWeek = firstDayObj.getDay(); 
    const lastDay = new Date(displayYear, displayMonth + 1, 0).getDate();

    for (let i = 0; i < startDayOfWeek; i++) {
        const emptyDiv = document.createElement('div');
        emptyDiv.className = 'cal-cell empty';
        grid.appendChild(emptyDiv);
    }

    for (let i = 1; i <= lastDay; i++) {
        const d = document.createElement('div');
        d.className = 'cal-cell';
        d.innerText = i;

        if (isCurrentMonth && i < realToday.getDate()) {
            d.classList.add('disabled');
        } else {
            d.onclick = function() {
                document.querySelectorAll('.cal-cell').forEach(c => c.classList.remove('selected'));
                d.classList.add('selected');
                const mStr = String(displayMonth + 1).padStart(2, '0');
                const dStr = String(i).padStart(2, '0');
                bookingData.date = `${displayYear}-${mStr}-${dStr}`;
                checkStep1();
            };
        }
        grid.appendChild(d);
    }
}

function selectTime(el, time) {
    document.querySelectorAll('.time-btn').forEach(b => b.classList.remove('selected'));
    el.classList.add('selected');
    bookingData.time = time;
    checkStep1();
}

function checkStep1() {
    const btn = document.getElementById('btnStep1');
    btn.disabled = !(bookingData.date && bookingData.time);
}

function calcEndTimes() {
    const btns = document.querySelectorAll('.time-btn');
    btns.forEach(btn => {
        const startStr = btn.dataset.start;
        const duration = parseInt(btn.dataset.duration); 
        if (!startStr || isNaN(duration)) return;
        const [h, m] = startStr.split(':').map(Number);
        const date = new Date();
        date.setHours(h);
        date.setMinutes(m + duration);
        const endH = String(date.getHours()).padStart(2, '0');
        const endM = String(date.getMinutes()).padStart(2, '0');
        const endSpan = btn.querySelector('.t-end');
        endSpan.innerText = `~ ${endH}:${endM}`;
    });
}

// --- STEP 2: 座席 ---
function renderSeats() {
    const map = document.getElementById('seatMap');
    const rows = ['A', 'B', 'C', 'D'];
    const cols = [1, 2, 3, 4, 5, 6, 7, 8];
    rows.forEach(row => {
        cols.forEach(col => {
            const id = row + col;
            const s = document.createElement('div');
            s.className = 'seat';
            s.onclick = () => toggleSeat(s, id);
            map.appendChild(s);
        });
    });
}

function toggleSeat(el, id) {
    if (bookingData.seats.includes(id)) {
        bookingData.seats = bookingData.seats.filter(s => s !== id);
        el.classList.remove('selected');
    } else {
        if (bookingData.seats.length >= 4) return alert("一度に予約できるのは4席までです");
        bookingData.seats.push(id);
        el.classList.add('selected');
    }
    updateSeatCards();
    document.getElementById('btnStep2').disabled = bookingData.seats.length === 0;
    bookingData.needFormUpdate = true;
}

function updateSeatCards() {
    for (let i = 0; i < 4; i++) {
        const slot = document.getElementById(`seat-slot-${i}`);
        const seatId = bookingData.seats[i]; 
        if (seatId) {
            slot.innerText = seatId;
            slot.classList.add('filled');
        } else {
            slot.innerText = "未選択";
            slot.classList.remove('filled');
        }
    }
}

// --- 画面遷移 ---
function goStep(step) {
    // STEP 3に行く直前にフォームを生成
    if (step === 3 && bookingData.needFormUpdate) {
        renderPassengerForms();
        calcTotal(); 
        bookingData.needFormUpdate = false;
    }

    document.querySelectorAll('.step-content').forEach(el => el.classList.remove('active'));
    document.getElementById('step' + step).classList.add('active');

    // ★追加: 画面のトップへスクロールする
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// --- STEP 3: フォーム生成 ---
function renderPassengerForms() {
    const container = document.getElementById('passengerForms');
    container.innerHTML = "";
    
    bookingData.seats.forEach((seat) => {
        const html = `
        <div class="ticket-card">
            <div class="seat-badge">${seat}</div>
            <div class="form-group">
                <div class="form-row">
                    <input type="text" class="inp-name" placeholder="お名前" required>
                    <select class="inp-member" onchange="calcTotal()">
                        <option value="0">非会員</option>
                        <option value="1">会員</option>
                    </select>
                </div>
                <div class="form-row">
                    <input type="number" class="inp-age" placeholder="年齢" onchange="calcTotal()" required>
                </div>
            </div>
        </div>`;
        container.insertAdjacentHTML('beforeend', html);
    });
}

// --- API計算 ---
async function calcTotal() {
    const names = document.querySelectorAll('.inp-name');
    const ages = document.querySelectorAll('.inp-age');
    const members = document.querySelectorAll('.inp-member');
    const coupon = document.getElementById('couponInput').value;
    const postCoupon = document.getElementById('postCoupon');
    if (postCoupon) {
        postCoupon.value = coupon;
    }
    
    const ageList = [];
    const memberList = [];
    let allFilled = true;

    ages.forEach((el, i) => {
        if (!el.value) allFilled = false;
        ageList.push(parseInt(el.value) || 0);
        memberList.push(parseInt(members[i].value));
    });

    if (!allFilled) return; 

    try {
        const res = await fetch('/api/calc', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                movie_id: MOVIE_ID,
                ages: ageList,
                is_members: memberList,
                coupon_code: coupon
            })
        });
        
        const data = await res.json();
        
        const errorBox = document.getElementById('errorMsg');
        const priceBox = document.getElementById('totalPriceDisplay');
        const subtotalBox = document.getElementById('subtotalDisplay');
        const discountBox = document.getElementById('discountDisplay');
        const btn = document.getElementById('btnSubmit');

        if (data.status === 'error') {
            errorBox.innerText = data.message;
            errorBox.style.display = 'block';
            priceBox.innerText = "---";
            subtotalBox.style.display = 'none'; 
            discountBox.innerText = "";
            btn.disabled = true; 
            btn.style.backgroundColor = "#ccc";
        } else {
            errorBox.style.display = 'none';
            priceBox.innerText = `¥${data.total_price.toLocaleString()}`;
            if (data.discount > 0) {
                subtotalBox.innerText = `¥${data.subtotal.toLocaleString()}`;
                subtotalBox.style.display = 'block'; 
                discountBox.innerText = `(クーポン適用 -¥${data.discount})`;
            } else {
                subtotalBox.style.display = 'none'; 
                discountBox.innerText = "";
            }

            btn.disabled = false;
            btn.style.backgroundColor = "#2d3436"; 
            const footerPrice = document.querySelector('#fixedFooter .footer-price');
            if(footerPrice) footerPrice.innerText = `¥${data.total_price.toLocaleString()}`;
        }

    } catch (e) {
        console.error(e);
    }
}

// --- 送信 ---
function submitOrder() {
    alert("送信ボタンが押されました！");
    const form = document.getElementById('finalForm');
    document.getElementById('postDate').value = `${bookingData.date} ${bookingData.time}`;
    document.getElementById('postSeat').value = bookingData.seats.join(",");
    
    const names = document.querySelectorAll('.inp-name');
    const ages = document.querySelectorAll('.inp-age');
    const members = document.querySelectorAll('.inp-member');
    const couponValue = document.getElementById('couponInput').value;
        console.log("送信するクーポン:", couponValue); 
    document.getElementById('postCoupon').value = couponValue;
    
    for(let n of names) {
        if(!n.value) return alert("お名前を入力してください");
    }

    names.forEach(el => addHidden(form, "names", el.value));
    ages.forEach(el => addHidden(form, "ages", el.value));
    members.forEach(el => addHidden(form, "is_members", el.value));
    
    form.submit();
}

function addHidden(form, name, value) {
    const i = document.createElement('input');
    i.type = 'hidden';
    i.name = name;
    i.value = value;
    form.appendChild(i);
}