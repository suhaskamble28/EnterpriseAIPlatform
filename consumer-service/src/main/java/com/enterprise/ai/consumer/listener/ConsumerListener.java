package com.enterprise.ai.consumer.listener;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;
import org.springframework.kafka.support.KafkaHeaders;
import org.springframework.messaging.handler.annotation.Header;


@Component
public class ConsumerListener {
	
	@Value("${instance.name}")
	private String instanceName;

	@KafkaListener(
	        topics = "user-events",
	        groupId = "group-1")
	public void consume(String message) {

	    System.out.println();
	    System.out.println("==========================================");
	    System.out.println("Received : " + message);

	    if (message.contains("FAIL")) {

	        System.out.println("Business Processing Failed...");

	        throw new RuntimeException("Simulated Exception");
	    }

	    System.out.println("Business Processing Successful");
	    System.out.println("==========================================");
	}
}