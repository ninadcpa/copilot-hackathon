package com.example.okta_demo_v1.service;

import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.http.*;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

public class OktaTokenServiceTest {

    @Mock
    private RestTemplate restTemplate;

    @InjectMocks
    private OktaTokenService oktaTokenService;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void getAccessToken_returnsToken_whenResponseIsValid() {
        String expectedToken = "mocked-token";
        String tokenUrl = "https://dev-16565142.okta.com/oauth2/default/v1/token";

        HttpHeaders headers = new HttpHeaders();
        headers.setBasicAuth("your-client-id", "your-client-secret");
        headers.set("Content-Type", "application/x-www-form-urlencoded");

        MultiValueMap<String, String> body = new LinkedMultiValueMap<>();
        body.add("grant_type", "client_credentials");
        body.add("scope", "api://default");

        HttpEntity<MultiValueMap<String, String>> request = new HttpEntity<>(body, headers);
        ResponseEntity<Map> responseEntity = new ResponseEntity<>(Map.of("access_token", expectedToken), HttpStatus.OK);

        when(restTemplate.exchange(tokenUrl, HttpMethod.POST, request, Map.class)).thenReturn(responseEntity);

        String actualToken = oktaTokenService.getAccessToken();

        assertEquals(expectedToken, actualToken);
    }

    @Test
    void getAccessToken_throwsException_whenResponseIsInvalid() {
        String tokenUrl = "https://dev-16565142.okta.com/oauth2/default/v1/token";

        HttpHeaders headers = new HttpHeaders();
        headers.setBasicAuth("your-client-id", "your-client-secret");
        headers.set("Content-Type", "application/x-www-form-urlencoded");

        MultiValueMap<String, String> body = new LinkedMultiValueMap<>();
        body.add("grant_type", "client_credentials");
        body.add("scope", "api://default");

        HttpEntity<MultiValueMap<String, String>> request = new HttpEntity<>(body, headers);

        when(restTemplate.exchange(tokenUrl, HttpMethod.POST, request, Map.class)).thenThrow(new RuntimeException("Invalid response"));

        assertThrows(RuntimeException.class, () -> oktaTokenService.getAccessToken());
    }
}
