# Overview

### Prerequisites

To build this solution you will need:

- An Azure subscription - <a href="https://azure.microsoft.com/free/cognitive-services" target="_blank">Create one for free</a>
- Access granted to Azure OpenAI in the desired Azure subscription
- A GitHub account and basic git knowledge to create repositories and commit files.

## Azure OpenAI deployment

### Create resource

Currently, access to this service is granted only by application. You can apply for access to Azure OpenAI by completing the form at <a href="https://aka.ms/oai/access" target="_blank">https://aka.ms/oai/access</a>. Open an issue on this repo to contact us if you have an issue.

1. Navigate to the create page: [Azure OpenAI Service Create Page](https://portal.azure.com/?microsoft_azure_marketplace_ItemHideKey=microsoft_openai_tip#create/Microsoft.CognitiveServicesOpenAI)
2. On the **Create** page provide the following information:

    |Field| Description   |
    |--|--|
    | **Subscription** | Select the Azure subscription used in your OpenAI onboarding application|
    | **Resource group** | The Azure resource group that will contain your OpenAI resource. You can create a new group or add it to a pre-existing group. |
    | **Region** | The location of your instance. Different locations may introduce latency, but have no impact on the runtime availability of your resource.|
    | **Name** | A descriptive name for your Azure services resource. For example, *MyQuoteGeneratorOpenAI*. |
    | **Pricing Tier** | Only 1 pricing tier is available for the service currently |
 
### Deploy a model

Before you can generate text or inference, you need to deploy a model. You can select from one of several available models in Azure OpenAI Studio.

To deploy a model, follow these steps:

1. Sign in to [Azure OpenAI Studio](https://oai.azure.com).
2. Select the subscription and Azure OpenAI resource to work with.
3. Under **Management** select **Deployments**.
4. Select **Create new deployment**.
5. Select either _gpt-35-turbo_ or _gpt-35-turbo-16k_ as a base model from the drop-down.
6. Enter a deployment name to help you identify the model. Save the name. as it will be used within the Azure Logic App to call the model via the REST API.
7. For your first deployment leave the Advanced Options set to the defaults.

The deployments table displays a new entry that corresponds to this newly created model. Your deployment status will move to succeeded when the deployment is complete and ready for use.

### Copy *endpoint* and *key*

To call our model via REST API from the Logic App, we need to copy the endpoint and key.\

1. Navigate to the OpenAI Settings page on Azure AI Studios' up right corner (cog icon). Click the *Resource* tab.
2. Select your resource and copy the *endpoint* value.
3. Click the eye icon on the Key column and copy the *key* value.

## Orchestrating your quote creation with Azure Logic Apps

### Create Azure Logic App
1. Navigate to the create page: [Azure Logic App Create Page](https://portal.azure.com/#create/Microsoft.LogicApp)
2. On the **Create Logic App** page provide the following information:

    |Field| Description   |
    |--|--|
    | **Subscription** | Select your Azure subscription |
    | **Resource group** | Select the Resource Group craeted in the steps above. |
    | **Logic App Name** | A descriptive name for your Azure Logic App resource. For example, *MyQuoteGeneratorLogicApp*. |
    | **Publish** | Pick Workflow.|
    | **Region** | The location of your instance. For latency resons, pick the same region where your OpenAI instance was created or the closest one possible.|
    | **Plan type** | For this simple demo, you can pick *Consumption*, for production deployments, consider a *Standard* plan. |

   Keep the other default selections by clicking *Review + Create*, review your selections and click *Create* after validation.

### Design your Logic App flow
1. Navigate to the Logic App code view.

   ![image](https://github.com/rochabr/openai-logicapps-quoteoftheday/assets/1051195/a098d3bd-4f27-4f6c-adf8-3cd705d9d8ff)

2. Copy the content from [workflow.json](workflow.json) and paste it as your Logic App code.  Replace _<OPENAI_ENDPOINT>_, _<OPENAI_MODEL>_ and _<OPENAI_KEY>_with the endpoint, model, and key from your OpenAI deployment, captured in the OpenAI Deployment step above.
3. Click *Save*.
4. Go to the *Logic App Designer*, select the _When a HTTP request is received_ and copy the *HTTP POST URL* value from it. We will use it in our HTML file, later.
   
## Hosting your web site with Azure Static Web App

We will create a very simple website to host an HTML file, connected to a new GitHub repository. For a more detailed tutorial on how to deploy static web apps using popular frameworks like Angular, Blazor, React and Vue, or to connect to an Azure DevOps repository, follow [this guide](https://learn.microsoft.com/en-us/azure/static-web-apps/get-started-portal?tabs=vanilla-javascript&pivots=github).

### Create new GitHub repository to host our HTML file

1. Follow the [Create a repo](https://docs.github.com/en/get-started/quickstart/create-a-repo) tutorial to create a new repository.
2. Copy the contents of [_index.html_](index.html) or download it.
3. Create a file with the same name within your repository's _main_ branch. Replace _<LOGIC_APP_URL>_ with the value from our Logic App *HTTP POST URL*.

### Connect your repo with an Azure Static Web App

1. Go to the [Azure portal](https://portal.azure.com).
2. Select **Create a Resource**.
3. Search for **Static Web Apps**.
4. Select **Static Web Apps**.
5. Select **Create**.

In the _Basics_ section, begin by configuring your new app and linking it to a GitHub repository.

| Setting | Value |
|--|--|
| Subscription | Select your Azure subscription. |
| Resource Group | Select the same resource group created in the beginning of the tutorial, or create a new one. |
| Name | Enter a name for your resource. You can use **my-quote-creator-web-app** in the textbox,for example. |
| Plan type | Select **Free**. |
| Azure Functions and staging details | Select a region closest to your previous deployments. |
| Source | Select **GitHub**. |

Select **Sign-in with GitHub** and authenticate with GitHub.

![image](https://github.com/rochabr/openai-logicapp-quotecreator/assets/1051195/a0542a6c-be60-41f7-bd0f-28f2610f99dc)

After you sign in with GitHub, enter the repository information.

| Setting | Value |
|--|--|
| Organization | Select your organization. |
| Repository| Select your repository name. |
| Branch | Select **<branch_name>**. |

> [!NOTE]
> If you don't see any repositories:
> - You may need to authorize Azure Static Web Apps in GitHub. Browse to your GitHub repository and go to **Settings > Applications > Authorized OAuth Apps**, select **Azure Static Web Apps**, and then select **Grant**.

In the _Build Details_ section, add configuration details specific to your preferred front-end framework.

1. Select **Custom** from the _Build Presets_ dropdown.
2. Type **/** in the _App location_ box.
3. Leave the _Api location_ box empty.
4. Type **/** _App artifact location_ box.

Select **Review + create**.

## View the website

There are two aspects to deploying a static app. The first creates the underlying Azure resources that make up your app. The second is a workflow that builds and publishes your application.

Before you can go to your new static site, the deployment build must first finish running.

The Static Web Apps *Overview* window displays a series of links that help you interact with your web app.

1. Selecting on the banner that says, _Select here to check the status of your GitHub Actions runs_ takes you to the GitHub Actions running against your repository. Once you verify the deployment job is complete, then you can go to your website via the generated URL.
2. Once GitHub Actions workflow is complete, you can select the _URL_ link to open the website in new tab.
3. Add comma-separated keywords in the input box and click *Build*.
4. After a few seconds, you'll see your quote with a related image in the background.

## Production considerations

1. Protect your resources with [VNets](Azure Virtual Private Network), [Managed Identity authentication and authrization](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/managed-identity).
2. Keep sensitive data like *service endpoints and keys* protected by using [Azure Key Vault](https://azure.microsoft.com/en-ca/products/key-vault) as an alternative.

## Clean up resources

If you're not going to continue to use this application, you can delete all your resurces through the following steps:

1. Open the [Azure portal](https://portal.azure.com).
2. Search for your *Resource Group* name from the top search bar. Open it.
4. Click **Delete resource group**.
5. Type the name of your resource group at the input box and click *Delete*.
