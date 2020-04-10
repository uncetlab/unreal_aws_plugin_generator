#pragma once

#include "CoreMinimal.h"

/*See https://sdk.amazonaws.com/cpp/api/0.14.3/struct_aws_1_1_client_1_1_client_configuration.html#a83473c30c3d35426c81af0f48653fd28
  for more info about each of the properties and default values
 */
#include "ClientConfiguration.generated.h"

USTRUCT(BlueprintType)
struct FClientConfiguration {
    GENERATED_USTRUCT_BODY()
 
    FClientConfiguration() :
        HttpScheme("https"),
        region("us-east-1"),
        useDualStack(false),
        maxConnections(25),
        requestTimeoutMs(3000),
        connectionTimeoutMs(1000)
    {}
public:
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AWS Client Configuration")
    FString HttpScheme;

    //change to a custom struct
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AWS Client Configuration")
    FString region;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AWS Client Configuration")
    bool useDualStack;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AWS Client Configuration")
    int32 maxConnections;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AWS Client Configuration")
    int32 requestTimeoutMs;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AWS Client Configuration")
    int32 connectionTimeoutMs;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AWS Client Configuration")
    FString endpointOverride;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AWS Client Configuration")
    FString proxyHost;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AWS Client Configuration")
    int32 proxyPort;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AWS Client Configuration")
    FString proxyUsername;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AWS Client Configuration")
    FString proxyPassword;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AWS Client Configuration")
    bool verifySSL;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AWS Client Configuration")
    FString caPath;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AWS Client Configuration")
    bool followRedirects;


};