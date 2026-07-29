package com.enterprise.ai.consumer.listener;

import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Component
public class ConsumerListener {

    @KafkaListener(
            topics = "user-events",
            groupId = "group-1")
    public void consume(String message) {

        System.out.println(
                "Received : " + message);
    }
}