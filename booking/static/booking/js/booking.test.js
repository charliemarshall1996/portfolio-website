/**
 * @jest-environment jsdom
 */

import {
    getCookie,
    generateTimeSlots,
    bookingSelectAllow,
    bookingFormSubmission,
    dateClickGet
} from './booking.js';

global.fetch = jest.fn();

describe('getCookie', () => {
    beforeEach(() => {
        Object.defineProperty(document, 'cookie', {
            writable: true,
            value: 'csrftoken=test123; sessionid=abc456'
        });
    });

    test('returns correct cookie value', () => {
        expect(getCookie('csrftoken')).toBe('test123');
        expect(getCookie('sessionid')).toBe('abc456');
    });

    test('returns null for nonexistent cookie', () => {
        expect(getCookie('nonexistent')).toBeNull();
    });
});

describe('generateTimeSlots', () => {
    let select;

    beforeEach(() => {
        document.body.innerHTML = '<select id="testSlot"></select>';
        select = $('#testSlot');
    });

    test('generates slots excluding booked ones', () => {
        generateTimeSlots(['09:15:00', '10:00:00'], select);

        const values = select.find('option').map((_, el) => el.value).get();
        expect(values).not.toContain('09:15:00');
        expect(values).not.toContain('10:00:00');
        expect(values).toContain('09:00:00');
        expect(values).toContain('09:45:00');
    });

    test('generates correct number of slots for unbooked day', () => {
        generateTimeSlots([], select);
        expect(select.find('option').length).toBe(32); // 8 hours * 4 slots = 32
    });
});

describe('bookingSelectAllow', () => {
    test('allows one-day selections not in the past', () => {
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const tomorrow = new Date(today.getTime() + 86400000);

        expect(bookingSelectAllow({ start: today, end: tomorrow })).toBe(true);
    });

    test('disallows multi-day selections', () => {
        const start = new Date();
        const end = new Date(start.getTime() + 2 * 86400000); // 2-day span
        expect(bookingSelectAllow({ start, end })).toBe(false);
    });

    test('disallows past selections', () => {
        const start = new Date(Date.now() - 86400000); // yesterday
        const end = new Date();
        expect(bookingSelectAllow({ start, end })).toBe(false);
    });
});

describe('bookingFormSubmission', () => {
    let form, selectedDateInput, mockEvent;

    beforeEach(() => {
        document.body.innerHTML = `
            <form id="bookingForm">
                <input name="name" value="Alice" />
                <input name="time" value="09:00:00" />
            </form>
            <input id="selectedDate" value="2024-12-25" />
        `;

        form = $('#bookingForm');
        selectedDateInput = $('#selectedDate');

        mockEvent = {
            preventDefault: jest.fn()
        };

        fetch.mockClear();
        fetch.mockResolvedValue({
            json: () => Promise.resolve({ status: 'ok' }),
        });
    });

    test('submits form data as JSON', async () => {
        await bookingFormSubmission.call(form, mockEvent, '/booking/', selectedDateInput);

        expect(mockEvent.preventDefault).toHaveBeenCalled();

        expect(fetch).toHaveBeenCalledWith('/booking/2024-12-25/', expect.objectContaining({
            method: 'POST',
            headers: expect.objectContaining({
                'Content-Type': 'application/json',
                'X-CSRFToken': expect.any(String)
            }),
            body: JSON.stringify({
                name: 'Alice',
                time: '09:00:00',
                date: '2024-12-25'
            })
        }));
    });
});

describe('dateClickGet', () => {
    let timeSlotSelect, selectedDateInput;

    beforeEach(() => {
        document.body.innerHTML = `
            <select id="timeSlot"></select>
            <input id="selectedDate" />
        `;

        timeSlotSelect = $('#timeSlot');
        selectedDateInput = $('#selectedDate');

        fetch.mockClear();
    });

    test('fetches available times and updates options', async () => {
        fetch.mockResolvedValueOnce({
            json: () => Promise.resolve({ booked_times: ['09:15:00', '10:00:00'] })
        });

        const info = { startStr: '2024-12-25' };
        await dateClickGet(info, timeSlotSelect, '/booking/', selectedDateInput);

        expect(selectedDateInput.val()).toBe('2024-12-25');
        expect(fetch).toHaveBeenCalledWith('/booking/2024-12-25/', expect.any(Object));

        const options = timeSlotSelect.find('option').map((_, el) => el.value).get();
        expect(options).toContain('09:00:00');
        expect(options).not.toContain('09:15:00');
    });
});
