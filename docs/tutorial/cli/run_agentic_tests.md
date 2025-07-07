In this tutorial, you will learn how to run an agentic test in Moonshot. Agentic tests are a set of instructions that can help to evaluate and assess the capabilities and safety of agentic models.

1. Change directory to the root directory of Moonshot.

2. Enter the following command to enter the CLI interactive mode:

        python -m moonshot cli interactive

3. Choose a type to run and view help:

    > **Warning**<br>
    <b>Important information before running your agentic tests:</b>
    <br><br>Certain agentic tests may require metrics that connect to a particular model, i.e. Joint Testing 3 cookbooks and recipes like [jt3-fraud-en](https://github.com/sgaisi/moonshot-data-aisi/blob/main/recipes/jt3-fraud-en.json) use the metric [jointtesting3](https://github.com/sgaisi/moonshot-data-aisi/blob/main/metrics/jointtesting3.py), which requires the API tokens of [together-gemma2-27b](https://github.com/sgaisi/moonshot-data-aisi/blob/main/connectors-endpoints/together-gemma2-27b.json) and [amazon-bedrock-anthropic-claude-3-7-sonnet-connector](https://github.com/sgaisi/moonshot-data-aisi/blob/main/connectors-endpoints/amazon-bedrock-anthropic-claude-3-7-sonnet-connector.json) endpoints.
    <br><br>Refer to this [list for the requirements](../../faq.md#requirements).

    - Recipe

        To find out more about the required fields to create a recipe:

            run_recipe -h

        To run an agentic example, enter:

            run_recipe "my new recipe runner" "['jt3-fraud-en']" "['openai-gpt4o']" -l agentic -n 1 -r 1 -s ""


    - Cookbook:

        To find out more about the required fields to create a cookbook:

            run_cookbook -h

        To run an agentic example, enter:

            run_cookbook "my new cookbook runner" "['AISI-JT3-en']" "['openai-gpt4o']" -l agentic -n 1 -r 1 -s ""


4. View the results:
    - Recipe:

        ![recipe results](images/recipe_results_table.png)

    - Cookbook:

        ![cookbook results](images/cookbook_results_table.png)

You can view more information on running agentic tests [here](../../user_guide/cli/agentic.md).