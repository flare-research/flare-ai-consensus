import structlog
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from flare_ai_consensus.consensus import run_consensus
from flare_ai_consensus.router import AsyncOpenRouterProvider
from flare_ai_consensus.settings import ConsensusConfig, Message

logger = structlog.get_logger(__name__)
router = APIRouter()


class ChatMessage(BaseModel):
    """
    Pydantic model for chat message validation.

    Attributes:
        message (str): The chat message content, must not be empty
    """

    system_message: str = Field(..., min_length=1)
    user_message: str = Field(..., min_length=1)


class ChatRouter:
    """
    A simple chat router that processes incoming messages using the CL pipeline.
    """

    def __init__(
        self,
        router: APIRouter,
        provider: AsyncOpenRouterProvider,
        consensus_config: ConsensusConfig | None = None,
    ) -> None:
        """
        Initialize the ChatRouter.

        Args:
            router (APIRouter): FastAPI router to attach endpoints.
            provider: instance of an async OpenRouter client.
            consensus_config: config for running the consensus algorithm.
        """
        self._router = router
        self.provider = provider
        if consensus_config:
            self.consensus_config = consensus_config
        self.logger = logger.bind(router="chat")
        self._setup_routes()

    def _setup_routes(self) -> None:
        """
        Set up FastAPI routes for the chat endpoint.
        """

        @self._router.post("/")
        async def chat(message: ChatMessage) -> dict[str, str] | None:  # pyright: ignore [reportUnusedFunction]
            """
            Process a chat message through the CL pipeline.
            Returns an aggregated response after a number of iterations.
            """
            try:
                self.logger.debug("Received chat message", message=message.user_message)
                # Build initial conversation
                initial_conversation: list[Message] = [
                    {"role": "system", "content": message.system_message},
                    {"role": "user", "content": message.user_message},
                ]

                # Run consensus algorithm
                answer = await run_consensus(
                    self.provider,
                    self.consensus_config,
                    initial_conversation,
                )

            except Exception as e:
                self.logger.exception("Chat processing failed", error=str(e))
                raise HTTPException(status_code=500, detail=str(e)) from e
            else:
                self.logger.info("Response generated", answer=answer)
                return {"response": answer}

    @property
    def router(self) -> APIRouter:
        """Return the underlying FastAPI router with registered endpoints."""
        return self._router
