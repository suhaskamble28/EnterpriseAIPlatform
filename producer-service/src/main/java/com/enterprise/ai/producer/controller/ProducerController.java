package com.enterprise.ai.producer.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ProducerController {

    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;

    @GetMapping("/publish")
    public String publish() {

        kafkaTemplate.send(
                "user-events",
                "Suhas started Day-46");

        return "Message Published Successfully";
    }
}