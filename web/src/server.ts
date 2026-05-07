import { createWorkersAI } from "workers-ai-provider";
import { callable, routeAgentRequest } from "agents";
import { AIChatAgent, type OnChatMessageOptions } from "@cloudflare/ai-chat";
import {
  convertToModelMessages,
  pruneMessages,
  stepCountIs,
  streamText
} from "ai";

export class ChatAgent extends AIChatAgent<Env> {
  maxPersistedMessages = 100;

  onStart() {
    // Configure OAuth popup behavior for MCP servers that require authentication
    this.mcp.configureOAuthCallback({
      customHandler: (result) => {
        if (result.authSuccess) {
          return new Response("<script>window.close();</script>", {
            headers: { "content-type": "text/html" },
            status: 200
          });
        }
        return new Response(
          `Authentication Failed: ${result.authError || "Unknown error"}`,
          { headers: { "content-type": "text/plain" }, status: 400 }
        );
      }
    });

    // Auto-connect to the cv-mcp server (idempotent — safe on restart)
    this.addMcpServer("cv-mcp", "https://mcp.francescoforesta.com/mcp", {
      transport: { type: "streamable-http" }
    });
  }

  @callable()
  async addServer(name: string, url: string) {
    return await this.addMcpServer(name, url);
  }

  @callable()
  async removeServer(serverId: string) {
    await this.removeMcpServer(serverId);
  }

  async onChatMessage(_onFinish: unknown, options?: OnChatMessageOptions) {
    const mcpTools = this.mcp.getAITools();
    const workersai = createWorkersAI({ binding: this.env.AI });

    const result = streamText({
      model: workersai("@cf/moonshotai/kimi-k2.6", {
        sessionAffinity: this.sessionAffinity
      }),
      system: `You are an assistant that answers questions about Francesco Foresta's professional background. You have access to MCP tools that expose his CV as structured markdown sections.

When a user asks a question:
1. Use list_sections to discover what's available.
2. Use get_section to fetch a section in full.
3. Use search for free-text questions where you don't know which section is relevant.

Compose multiple tool calls when needed. It's better to make two focused calls than to guess from one.

Answer in English. Be factual and concise. If the data does not contain an answer, say so directly without speculating. Do not embellish or characterize the work in promotional language.

The audience is professional contacts — recruiters, peers, partners. Tone is sober and informative. Default to short paragraphs of prose; use bullet lists only when the user explicitly asks for a list or when the answer is genuinely a list of items.`,
      messages: pruneMessages({
        messages: await convertToModelMessages(this.messages),
        toolCalls: "before-last-2-messages"
      }),
      tools: {
        ...mcpTools
      },
      stopWhen: stepCountIs(5),
      abortSignal: options?.abortSignal
    });

    return result.toUIMessageStreamResponse();
  }
}

export default {
  async fetch(request: Request, env: Env) {
    return (
      (await routeAgentRequest(request, env)) ||
      new Response("Not found", { status: 404 })
    );
  }
} satisfies ExportedHandler<Env>;
