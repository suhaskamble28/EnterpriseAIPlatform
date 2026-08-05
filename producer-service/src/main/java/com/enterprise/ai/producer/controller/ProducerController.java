package com.enterprise.ai.producer.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import com.enterprise.ai.producer.model.OrderEvent;

@RestController
public class ProducerController {
	
	private int counter = 1;


 //   @Autowired
   // private KafkaTemplate<String, String> kafkaTemplate;
    
   @Autowired
   private KafkaTemplate<String, OrderEvent> kafkaTemplate;

    @GetMapping("/publish")
    public String publish() {

        OrderEvent[] events = {

                new OrderEvent(
                        "MSG-004",
                        "ORD-1001",
                        "CUST-101",
                        "ORDER_CREATED",
                        2500),

                new OrderEvent(
                        "MSG-005",
                        "ORD-1002",
                        "CUST-102",
                        "PAYMENT_SUCCESS",
                        4800),

                new OrderEvent(
                        "MSG-006",
                        "ORD-1003",
                        "CUST-103",
                        "SHIPMENT_STARTED",
                        3500),

                // Duplicate Event
                new OrderEvent(
                        "MSG-004",
                        "ORD-1002",
                        "CUST-102",
                        "PAYMENT_SUCCESS",
                        4800)
        };

        for (OrderEvent event : events) {

            kafkaTemplate.send(
            		"order-events",
                    event.getEventId(),
                    event);

            System.out.println("Published : " + event.getEventId());
        }

        return "Order Events Published Successfully";
    }
}
    
    
    
    
    
 