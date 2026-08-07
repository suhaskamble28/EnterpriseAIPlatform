package com.enterprise.ai.consumer.config;

import com.enterprise.ai.consumer.model.OrderEvent;
import com.enterprise.ai.consumer.error.KafkaErrorHandlerConfig;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory;
import org.springframework.kafka.core.ConsumerFactory;
import org.springframework.kafka.core.DefaultKafkaConsumerFactory;
import org.springframework.kafka.support.serializer.JsonDeserializer;
import org.springframework.kafka.listener.DefaultErrorHandler;

import java.util.HashMap;
import java.util.Map;

@Configuration
public class KafkaConsumerConfig {

	KafkaErrorHandlerConfig conf = new KafkaErrorHandlerConfig();
	 
    @Bean
    public ConsumerFactory<String, OrderEvent> consumerFactory() {
    	
    	System.out.println("***** CUSTOM CONSUMER FACTORY LOADED *****");

        Map<String, Object> props = new HashMap<>();

        props.put(
                ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG,
                "localhost:9092");

        props.put(
                ConsumerConfig.GROUP_ID_CONFIG,
                "group-1");

        props.put(
                ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG,
                StringDeserializer.class);

        props.put(
                ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG,
                JsonDeserializer.class);

        props.put(
                JsonDeserializer.TRUSTED_PACKAGES,
                "com.enterprise.ai.consumer.model");
        
        props.put(JsonDeserializer.TRUSTED_PACKAGES, "*");

        props.put(
                JsonDeserializer.VALUE_DEFAULT_TYPE,
                "com.enterprise.ai.consumer.model.OrderEvent");

        props.put(
                JsonDeserializer.USE_TYPE_INFO_HEADERS,
                false);

        return new DefaultKafkaConsumerFactory<>(
                props,
                new StringDeserializer(),
                new JsonDeserializer<>(OrderEvent.class));
    }

   
    @Bean
    public ConcurrentKafkaListenerContainerFactory<String, OrderEvent>
    kafkaListenerContainerFactory(
    				DefaultErrorHandler errorHandler) {

        System.out.println("***** CUSTOM LISTENER FACTORY LOADED *****");

        ConcurrentKafkaListenerContainerFactory<String, OrderEvent> factory =
                new ConcurrentKafkaListenerContainerFactory<>();

        factory.setConsumerFactory(consumerFactory());

        // Connect our custom retry + DLT error handler
        factory.setCommonErrorHandler(errorHandler);

        return factory;
    }
}