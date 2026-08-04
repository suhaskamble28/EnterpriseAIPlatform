package com.enterprise.ai.consumer.config;

import java.util.Collection;

import org.apache.kafka.clients.consumer.ConsumerRebalanceListener;
import org.apache.kafka.common.TopicPartition;

public class LoggingRebalanceListener implements ConsumerRebalanceListener {

    @Override
    public void onPartitionsRevoked(Collection<TopicPartition> partitions) {

        System.out.println();
        System.out.println("========================================");
        System.out.println("REBALANCE STARTED");
        System.out.println("Partitions Revoked");
        System.out.println("========================================");

        partitions.forEach(partition ->

                System.out.println(
                        partition.topic()
                        + " - Partition "
                        + partition.partition()));

        System.out.println();
    }

    @Override
    public void onPartitionsAssigned(Collection<TopicPartition> partitions) {

        System.out.println();
        System.out.println("========================================");
        System.out.println("REBALANCE COMPLETED");
        System.out.println("Partitions Assigned");
        System.out.println("========================================");

        partitions.forEach(partition ->

                System.out.println(
                        partition.topic()
                        + " - Partition "
                        + partition.partition()));

        System.out.println();
    }
}