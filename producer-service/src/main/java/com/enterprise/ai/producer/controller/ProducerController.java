package com.enterprise.ai.producer.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ProducerController {
	
	private int counter = 1;


    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;

    @GetMapping("/publish")
    
    public String publish() {

        String key = "USER-" + (counter % 3);

        String message = "Message-" + counter++;

     /*   kafkaTemplate.send(
                "user-events",
                key,
                message);  */
        
        kafkaTemplate.send(
                "user-events",
                key,
                "FAIL-1");  

        return "Published : " + message;
    }
    
}  
    
    
    
    
    
 /*   public String publish() {
    	
    	  for (int i = 1; i <= 30; i++) {   // added for multiple messages

              String message = "Message-" + i;

             // kafkaTemplate.send("user-events", "Suhas started Day-46");
              
             kafkaTemplate.send("user-events", message);
              
            
          System.out.println("Published : " + message);

    	  }

         return "20 Messages Published Successfully";
    }
}  */