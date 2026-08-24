package com.enterprise.ai.producer.config;

import com.enterprise.ai.producer.model.OrderEvent;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.common.serialization.StringSerializer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.core.DefaultKafkaProducerFactory;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.core.ProducerFactory;
import org.springframework.kafka.support.serializer.JsonSerializer;

import java.util.HashMap;
import java.util.Map;

@Configuration
public class KafkaProducerConfig {

    @Bean
    public ProducerFactory<String, OrderEvent> producerFactory() {

        Map<String, Object> config = new HashMap<>();

        config.put(
                ProducerConfig.BOOTSTRAP_SERVERS_CONFIG,
                "localhost:9092");
       // Added for producer reliability
        
        config.put(
                ProducerConfig.ACKS_CONFIG,
                "all");
        
        config.put(
                ProducerConfig.RETRIES_CONFIG,
                3);
        
        config.put(
                ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG,
                true);

        // Added for producer reliability
     
        config.put(
                ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG,
                StringSerializer.class);

        config.put(
                ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG,
                JsonSerializer.class);
        
        config.put(
                JsonSerializer.ADD_TYPE_INFO_HEADERS,
                false);
        
     // Added for producer transaction ID
        
      /*  config.put(
                ProducerConfig.TRANSACTIONAL_ID_CONFIG,
                "producer-service-tx-");  */

        return new DefaultKafkaProducerFactory<>(config);
    }

    @Bean
    public KafkaTemplate<String, OrderEvent> kafkaTemplate() {
        return new KafkaTemplate<>(producerFactory());
    }
}