#include "Serializer.h"


Aws::String AWSSerializer::FStoAS(FString s) {
	return Aws::String(TCHAR_TO_UTF8(*s));
}

FString AWSSerializer::AStoFS(Aws::String s) {
	return FString(s.c_str());
}

const Aws::Client::ClientConfiguration AWSSerializer::ClientConfiguration(FClientConfiguration config) {
	Aws::Client::ClientConfiguration awsClient;
	awsClient.scheme = Aws::Http::SchemeMapper::FromString(TCHAR_TO_UTF8(*config.HttpScheme));
	awsClient.region = AWSSerializer::FStoAS(config.region);
	awsClient.useDualStack = config.useDualStack;
	awsClient.maxConnections = config.maxConnections;
	awsClient.requestTimeoutMs = config.requestTimeoutMs;
	awsClient.connectTimeoutMs = config.connectionTimeoutMs;
	awsClient.endpointOverride = AWSSerializer::FStoAS(config.endpointOverride);
	awsClient.proxyHost = AWSSerializer::FStoAS(config.proxyHost);
	awsClient.proxyPort = config.proxyPort;
	awsClient.proxyUserName = AWSSerializer::FStoAS(config.proxyUsername);
	awsClient.proxyPassword = AWSSerializer::FStoAS(config.proxyPassword);
	awsClient.verifySSL = config.verifySSL;
	awsClient.caPath = AWSSerializer::FStoAS(config.caPath);
	awsClient.followRedirects = config.followRedirects;
	
	return awsClient;
}

const Aws::Auth::AWSCredentials AWSSerializer::Credentials(FCredentials credentials) {
	Aws::Auth::AWSCredentials awsCredentials;
	awsCredentials.SetAWSAccessKeyId(AWSSerializer::FStoAS(credentials.AWSAcessKeyId));
	awsCredentials.SetAWSSecretKey(AWSSerializer::FStoAS(credentials.AWSSecretKey));
	awsCredentials.SetSessionToken(AWSSerializer::FStoAS(credentials.SessionToken));

	return awsCredentials;
}

void* AWSSerializer::NoChange(void* in) {
	return in;
}

Aws::String* AWSSerializer::PFStoPAS(FString* s) {
	char* tmp = new char[s->GetAllocatedSize()];
	strcpy(tmp, TCHAR_TO_UTF8(**s));
	auto rv = new Aws::String(tmp);

	return rv;
}


FString* AWSSerializer::PAStoPFS(Aws::String* s) {
	auto rv = new FString(s->c_str());

	return rv;
}