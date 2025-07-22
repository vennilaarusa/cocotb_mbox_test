# Mailbox Verification – Test Plan

| **Feature**        | **Test ID**    | **Input Conditions**           | **Expected Output**       | **Corner Cases**           |
|--------------------|----------------|--------------------------------|----------------------------|----------------------------|
| Enqueue Operation  | MBOX_ENQ_01    | Valid data, enqueue signal     | Data written to FIFO       | Enqueue when full          |
| Dequeue Operation  | MBOX_DEQ_01    | Dequeue signal asserted        | Data read from FIFO        | Dequeue when empty         |
| Status Register    | MBOX_STAT_01   | Read status register           | Flags match FIFO state     | Rapid toggling of flags    |
