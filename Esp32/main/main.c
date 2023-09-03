//Curtis Instruments @ 2018

#include "main.h"
#include "mcp2515.h"
#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "esp_spi_flash.h"
#include "max30102.h"
//
#include <string.h>
#include "esp_event.h"
#include "esp_event_loop.h"
#include "nvs_flash.h"
#include "driver/gpio.h"
#include "mcp2515.h"
#include "sdkconfig.h"
#include "esp_attr.h"
//
#define I2C_SDA 21
#define I2C_SCL 22
#define I2C_FRQ 100000
#define I2C_PORT I2C_NUM_0
max30102_config_t max30102 = {};
uint8_t bio_data[8];
esp_err_t i2c_master_init(i2c_port_t i2c_port){
    i2c_config_t conf = {};
    conf.mode = I2C_MODE_MASTER;
    conf.sda_io_num = I2C_SDA;
    conf.scl_io_num = I2C_SCL;
    conf.sda_pullup_en = GPIO_PULLUP_ENABLE;
    conf.scl_pullup_en = GPIO_PULLUP_ENABLE;
    conf.master.clk_speed = I2C_FRQ;
    i2c_param_config(i2c_port, &conf);
    return i2c_driver_install(i2c_port, I2C_MODE_MASTER, 0, 0, 0);
}

void get_bpm(void* param) {
    printf("MAX30102 Test\n");
    max30102_data_t result = {};
    ESP_ERROR_CHECK(max30102_print_registers(&max30102));
    while(true) {
        //Update sensor, saving to "result"
        ESP_ERROR_CHECK(max30102_update(&max30102, &result));
        if(result.pulse_detected) {
            printf("BEAT\n");
            printf("BPM: %f | SpO2: %f%%\n", result.heart_bpm, result.spO2);
                memcpy(&bio_data[0], &result.heart_bpm, sizeof(float));
    memcpy(&bio_data[4], &result.spO2, sizeof(float));
            /*bio_data[0]=result.heart_bpm;
            bio_data[1]=result.spO2;*/
            mcp_send_can(0x7FF,bio_data,8);
        }
        //Update rate: 100Hz
        //mcp_send_can(0x123,test_data,8);
        vTaskDelay(10/portTICK_PERIOD_MS);
    }
}


void can_rx(void* arg)
{
    uint32_t io_num;
    for(;;)
    {
    	extern bool rx_has_data();
    	rx_has_data();

//        if(xQueueReceive(gpio_evt_queue, &io_num, portMAX_DELAY))
//        {
//            printf("GPIO[%d] intr, val: %d\n", io_num, gpio_get_level(io_num));
//        }
    	//printf("\nin1ms\n");
    	//xTaskSuspend();
    }
}

void app_main(void)
{
	printf("\r\n*******************************************\r\n");
	printf("\r\nTemplate for Curtis Instruments 1305 Canary\r\n");
	printf("\r\n*******************************************\r\n");
//Init I2C_NUM_0
    ESP_ERROR_CHECK(i2c_master_init(I2C_PORT));
    //Init sensor at I2C_NUM_0
    ESP_ERROR_CHECK(max30102_init( &max30102, I2C_PORT,
                   MAX30102_DEFAULT_OPERATING_MODE,
                   MAX30102_DEFAULT_SAMPLING_RATE,
                   MAX30102_DEFAULT_LED_PULSE_WIDTH,
                   MAX30102_DEFAULT_IR_LED_CURRENT,
                   MAX30102_DEFAULT_START_RED_LED_CURRENT,
                   MAX30102_DEFAULT_MEAN_FILTER_SIZE,
                   MAX30102_DEFAULT_PULSE_BPM_SAMPLE_SIZE,
                   MAX30102_DEFAULT_ADC_RANGE, 
                   MAX30102_DEFAULT_SAMPLE_AVERAGING,
                   MAX30102_DEFAULT_ROLL_OVER,
                   MAX30102_DEFAULT_ALMOST_FULL,
                   false ));


	mcp_init(BAUD_125);
	
	//mcp_send_can(0x7FF,test_data,8);
	xTaskCreate(get_bpm, "Get BPM", 8192, NULL, 1, NULL);
    //xTaskCreate(task_1ms, "1ms tic", 2048, NULL, 10, NULL);
    //xTaskCreate(can_rx, "canrx handler", 2048, NULL, 10, NULL);
    /*while(1)
    {
    	extern bool rx_has_data();
    	rx_has_data();
    }*/

}
