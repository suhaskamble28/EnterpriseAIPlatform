package com.enterprise.ai.consumer.listener;

import org.apache.kafka.clients.consumer.ConsumerRecord;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

import com.enterprise.ai.consumer.model.OrderEvent;

import org.springframework.kafka.support.KafkaHeaders;
import org.springframework.messaging.handler.annotation.Header;

import java.util.HashSet;
import java.util.Set;


@Component
public class ConsumerListener {
	
	@Value("${instance.name}")
	private String instanceName;
	private final Set<String> processedMessages = new HashSet<>();

	@KafkaListener(
	        topics = "order-events",
	        groupId = "group-1",
	        containerFactory = "kafkaListenerContainerFactory")
	
	public void consume(ConsumerRecord<String, OrderEvent> record) {

		OrderEvent event = record.value();

		System.out.println("\n==========================================");
		System.out.println("Received Event");
		System.out.println("------------------------------------------");
		System.out.println("Event Id    : " + event.getEventId());
		System.out.println("Order Id    : " + event.getOrderId());
		System.out.println("Customer Id : " + event.getCustomerId());
		System.out.println("Event Type  : " + event.getEventType());
		System.out.println("Amount      : " + event.getAmount());
		
		System.out.println("\n==========================================");
		System.out.println("Partition details");
		System.out.println("Instance : " + instanceName);
		System.out.println("Partition : " + record.partition());
		System.out.println("Offset : " + record.offset());

		if (processedMessages.contains(event.getEventId())) {

		    System.out.println("\nDuplicate Event Detected...");
		    System.out.println("Ignoring Event : " + event.getEventId());
		    System.out.println("==========================================");
		    return;
		}

		processedMessages.add(event.getEventId());
		
		// Added for Monitor Lag
		try {
		    Thread.sleep(5000);
		} catch (InterruptedException e) {
		    Thread.currentThread().interrupt();
		}

		System.out.println("\nBusiness Processing Successful");
		System.out.println("Saved Event ID : " + event.getEventId());
		System.out.println("==========================================");
	}
	/*public void consume(OrderEvent event) {

	    System.out.println("\n==========================================");
	    System.out.println("Received Event");
	    System.out.println("------------------------------------------");
	    System.out.println("Event Id    : " + event.getEventId());
	    System.out.println("Order Id    : " + event.getOrderId());
	    System.out.println("Customer Id : " + event.getCustomerId());
	    System.out.println("Event Type  : " + event.getEventType());
	    System.out.println("Amount      : " + event.getAmount());

	    if (processedMessages.contains(event.getEventId())) {

	        System.out.println("\nDuplicate Event Detected...");
	        System.out.println("Ignoring Event : " + event.getEventId());
	        System.out.println("==========================================");
	        return;
	    }

	    processedMessages.add(event.getEventId());

	    System.out.println("\nBusiness Processing Successful");
	    System.out.println("Saved Event ID : " + event.getEventId());
	    System.out.println("==========================================");
	}  */
}