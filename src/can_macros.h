#pragma once

#define INIT_MESSAGE(message) \
    message##_t message; \
    message##_init(&message)

#define PACK_MESSAGE(message, dst) \
    message##_pack(dst, &message, message##_length)

#define UNPACK_MESSAGE(message, src) \
    message##_unpack(&message, src, message##_length)

#define ENCODE_SIGNAL(message, signal, value) \
    message.signal = message##_##signal##_encode(value)

#define DECODE_SIGNAL(message, signal) \
    message##_##signal##_decode(message.signal)

#define IS_IN_RANGE(message, signal) \
    message##_##signal##_is_in_range(message.signal)

#define DECODE_MESSAGE(message) \
    decode_##message(const message##_t &message)

#define SEND_MESSAGE_H(message) \
    send_##message(message##_t message = [](){ INIT_MESSAGE(message); return message; }())

#define SEND_MESSAGE(message) \
    send_##message(message##_t message)
