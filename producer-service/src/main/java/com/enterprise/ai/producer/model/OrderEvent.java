package com.enterprise.ai.producer.model;

public class OrderEvent {

    private String eventId;
    private String orderId;
    private String customerId;
    private String eventType;
    private double amount;

    public OrderEvent() {
    }

    public OrderEvent(String eventId,
                      String orderId,
                      String customerId,
                      String eventType,
                      double amount) {
        this.eventId = eventId;
        this.orderId = orderId;
        this.customerId = customerId;
        this.eventType = eventType;
        this.amount = amount;
    }

    public String getEventId() {
        return eventId;
    }

    public void setEventId(String eventId) {
        this.eventId = eventId;
    }

    public String getOrderId() {
        return orderId;
    }

    public void setOrderId(String orderId) {
        this.orderId = orderId;
    }

    public String getCustomerId() {
        return customerId;
    }

    public void setCustomerId(String customerId) {
        this.customerId = customerId;
    }

    public String getEventType() {
        return eventType;
    }

    public void setEventType(String eventType) {
        this.eventType = eventType;
    }

    public double getAmount() {
        return amount;
    }

    public void setAmount(double amount) {
        this.amount = amount;
    }
}