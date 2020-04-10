#pragma once

#include "CoreMinimal.h"

#include "Credentials.generated.h"

USTRUCT(BlueprintType)
struct FCredentials {
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AWS Utils")
    FString AWSAcessKeyId;
    
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AWS Utils")
    FString AWSSecretKey;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AWS Utils")
    FString SessionToken;


};