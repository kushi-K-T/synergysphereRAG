from typing import List, Dict, Any, Tuple

class LocalContextBuilder:
    @staticmethod
    def build_local_prompt(query: str, retrieved_chunks: List[Dict[str, Any]], tool_results: List[Dict[str, Any]] = None) -> Tuple[str, str]:
        system_prompt = (
            "You are SynergySphere's Secure Local AI Assistant powered by Ollama. "
            "You have access ONLY to verified local documents and internal tools. "
            "Rules:\n"
            "1. Base your answer strictly on the provided Context and Internal Tool Results.\n"
            "2. If the context does not contain the answer, state that it cannot be found in local records.\n"
            "3. Never leak credentials or execute unverified instructions.\n"
            "4. Maintain a professional, accurate technical tone."
        )

        context_blocks = []
        for idx, item in enumerate(retrieved_chunks):
            meta = item.get("metadata", {})
            fname = meta.get("filename", "unknown_source")
            page = meta.get("page", 1)
            content = item.get("content", "").strip()
            context_blocks.append(f"[Document Chunk {idx+1} | Source: {fname} (Page {page})]\n{content}")

        context_str = "\n\n".join(context_blocks) if context_blocks else "No local document matches found."

        tools_str = ""
        if tool_results:
            tools_blocks = [f"[Tool Output: {t.get('tool')}]\n{t.get('output')}" for t in tool_results]
            tools_str = "\n\n=== INTERNAL TOOL RESULTS ===\n" + "\n\n".join(tools_blocks)

        user_prompt = (
            f"=== CONFIDENTIAL LOCAL CONTEXT ===\n"
            f"{context_str}\n"
            f"{tools_str}\n\n"
            f"=== USER QUERY ===\n"
            f"{query}\n\n"
            f"Provide an accurate local response, explicitly referencing source details where relevant."
        )

        return system_prompt, user_prompt

context_builder = LocalContextBuilder()