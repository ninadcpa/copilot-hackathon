package com.example.okta_demo_v1.service;


import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.http.*;
import org.springframework.test.util.ReflectionTestUtils;
import org.springframework.web.client.RestTemplate;

public class ApiServiceTest {

    @Mock
    private OktaTokenService oktaTokenService;

    @Mock
    private RestTemplate restTemplate;

    @InjectMocks
    private ApiService apiService;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void callApi_returnsResponseBody_whenRequestIsSuccessful() {
        String expectedResponse = "mocked-response";
        String accessToken = "mocked-token";
        String apiUrl = "https://api.example.com/endpoint";

        when(oktaTokenService.getAccessToken()).thenReturn(accessToken);

        HttpHeaders headers = new HttpHeaders();
        headers.setBearerAuth(accessToken);
        HttpEntity<String> entity = new HttpEntity<>(headers);

        ResponseEntity<String> responseEntity = new ResponseEntity<>(expectedResponse, HttpStatus.OK);
        ReflectionTestUtils.setField(  apiService, "restTemplate", restTemplate);
        when(restTemplate.exchange(any(),eq(String.class)  )).thenReturn(responseEntity);

        String actualResponse = apiService.callApi();

        assertEquals(expectedResponse, actualResponse);
    }

    @Test
    void callApi_throwsException_whenRequestFails() {
        String accessToken = "mocked-token";
        String apiUrl = "https://api.example.com/endpoint";

        when(oktaTokenService.getAccessToken()).thenReturn(accessToken);

        HttpHeaders headers = new HttpHeaders();
        headers.setBearerAuth(accessToken);
        HttpEntity<String> entity = new HttpEntity<>(headers);

        when(restTemplate.exchange(apiUrl, HttpMethod.GET, entity, String.class)).thenThrow(new RuntimeException("Request failed"));

        assertThrows(RuntimeException.class, () -> apiService.callApi());
    }
}

