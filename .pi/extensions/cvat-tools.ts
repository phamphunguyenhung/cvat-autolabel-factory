/**
 * Thin Pi Coding Agent extension adapter for cvat-tools v2.0.
 * Zero inference or CVAT business logic in TypeScript — delegates to `python -m cvat_tools ...`.
 */
export default function cvatToolsExtension(pi: any) {
  const runCli = async (args: string[], ctx: any) => {
    const res = await pi.exec("python", ["-m", "cvat_tools", ...args]);
    if (res.code !== 0) {
      ctx?.ui?.notify?.(`cvat-tools exited ${res.code}: ${res.stderr || res.stdout}`, "error");
    }
    return res;
  };

  pi.registerCommand("cvat-status", {
    description: "Check CVAT environment, RAM, and read-only server connectivity",
    handler: async (_args: string, ctx: any) => runCli(["doctor"], ctx),
  });

  pi.registerCommand("cvat-tools", {
    description: "List registered cvat-tools kernel tools and permissions",
    handler: async (_args: string, ctx: any) => runCli(["--json", "tools", "list"], ctx),
  });

  pi.registerCommand("cvat-prelabel", {
    description: "Run local read-only prelabel draft generation for a job (e.g. /cvat-prelabel 285)",
    handler: async (args: string, ctx: any) => {
      const job = args.trim() || "285";
      return runCli(["run", "--job", job], ctx);
    },
  });

  pi.registerCommand("cvat-validate", {
    description: "Show local ShapeStore stats/validation for a job (e.g. /cvat-validate 285)",
    handler: async (args: string, ctx: any) => {
      const job = args.trim() || "285";
      return runCli(["--json", "store", "stats", "--job", job], ctx);
    },
  });

  pi.registerCommand("cvat-review", {
    description: "Run dry-run push preview for a job (never writes without --yes)",
    handler: async (args: string, ctx: any) => {
      const job = args.trim() || "285";
      return runCli(["--json", "store", "push", "--job", job], ctx);
    },
  });
}
